from __future__ import annotations
import statistics

from homer import fuzzy
from homer.errors import MissingStructureError
from homer.location import Location
from homer.locations import TwoPointLocation
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.nodes import Concept


class ContextualSpace(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        contents: StructureCollection,
        conceptual_spaces: StructureCollection,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        is_main_input: bool = False,
    ):
        Space.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            contents=contents,
            quality=0.0,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
        )
        self.conceptual_spaces = conceptual_spaces
        self.is_main_input = is_main_input
        self.is_contextual_space = True

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "parent_id": self.parent_id,
            "contents": [item.structure_id for item in self.contents],
            "contents_repr": [str(item) for item in self.contents],
            "conceptual_spaces": [
                space.structure_id for space in self.conceptual_spaces
            ],
            "conceptual_space_names": [space.name for space in self.conceptual_spaces],
            "quality": self.quality,
            "activation": self.activation,
        }

    @property
    def quality(self):
        active_contents = self.contents.filter(lambda x: x.activation > 0.5)
        if active_contents.is_empty():
            return 0.0
        return statistics.fmean(
            [
                fuzzy.AND(structure.quality, structure.activation)
                for structure in active_contents
            ]
        )

    def add(self, structure: Structure):
        if structure not in self.contents:
            self.contents.add(structure)

    def decay_activation(self, amount: float = None):
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        for item in self.contents:
            item.decay_activation(amount)

    def update_activation(self):
        self._activation = (
            statistics.median([item.activation for item in self.contents])
            if len(self.contents) != 0
            else 0.0
        )

    def copy(self, **kwargs: dict) -> ContextualSpace:
        """Requires keyword arguments 'bubble_chamber' and 'parent_id'."""
        bubble_chamber = kwargs["bubble_chamber"]
        parent_id = kwargs["parent_id"]
        copies = kwargs.get("copies", {})
        new_space = bubble_chamber.new_contextual_space(
            parent_id=parent_id,
            name=self.name,
            parent_concept=self.parent_concept,
            conceptual_spaces=self.conceptual_spaces.copy(),
        )
        for old_item, new_item in copies.items():
            if old_item.has_location_in_space(self):
                old_location = old_item.location_in_space(self)
                try:
                    new_location = Location(old_location.coordinates, new_space)
                except NotImplementedError:
                    new_location = TwoPointLocation(
                        old_location.start_coordinates,
                        old_location.end_coordinates,
                        new_space,
                    )
                new_item.locations.append(new_location)
                new_item.parent_spaces.add(new_location.space)
                new_location.space.add(new_item)
        for item in self.contents.filter(lambda x: x.is_node and x not in copies):
            new_location = Location(item.location_in_space(self).coordinates, new_space)
            new_item, copies = item.copy_with_contents(
                copies=copies,
                bubble_chamber=bubble_chamber,
                parent_id=parent_id,
                new_location=new_location,
            )
            new_space.add(new_item)
            copies[item] = new_item
            for label in item.labels:
                new_label = label.copy(
                    start=new_item,
                    parent_space=new_space,
                    parent_id=parent_id,
                    bubble_chamber=bubble_chamber,
                )
                new_item.links_out.add(new_label)
                new_space.add(new_label)
                copies[label] = new_label
            for relation in item.links_out.where(is_relation=True):
                if relation.end not in copies:
                    continue
                new_end = copies[relation.end]
                new_relation = relation.copy(
                    start=new_item,
                    end=new_end,
                    parent_space=new_space,
                    bubble_chamber=bubble_chamber,
                )
                new_end.links_in.add(new_relation)
                new_item.links_out.add(new_relation)
                new_space.add(new_relation)
                copies[relation] = new_relation
            for relation in item.links_in.where(is_relation=True):
                if relation.start not in copies:
                    continue
                new_start = copies[relation.start]
                new_relation = relation.copy(
                    start=new_start,
                    end=new_item,
                    parent_space=new_space,
                    bubble_chamber=bubble_chamber,
                    parent_id=parent_id,
                )
                new_item.links_in.add(new_relation)
                new_start.links_out.add(new_relation)
                new_space.add(new_relation)
                copies[relation] = new_relation
            while True:
                try:
                    label = self.contents.filter(
                        lambda x: x.is_label and x.start in copies and x not in copies
                    ).get()
                    new_label = label.copy(
                        start=copies[label.start],
                        parent_space=new_space,
                        parent_id=parent_id,
                        bubble_chamber=bubble_chamber,
                    )
                    copies[label.start].links_out.add(new_label)
                    new_space.add(new_label)
                    copies[label] = new_label
                except MissingStructureError:
                    break
        return new_space, copies

    def to_long_string(self) -> str:
        string = "-" * 120 + "\n"
        string += f"{self.structure_id}\n"
        string += "-" * 120 + "\n"
        for structure in self.contents.where_not(is_correspondence=True):
            string += f"{structure}\n"
        return string
