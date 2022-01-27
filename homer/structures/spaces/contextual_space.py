from __future__ import annotations
import statistics

from homer.id import ID
from homer.location import Location
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
        self.is_contextual_space = True

    @property
    def quality(self):
        active_contents = {
            structure for structure in self.contents if structure.activation > 0
        }
        if len(active_contents) == 0:
            return 0.0
        return statistics.fmean(
            [structure.quality * structure.activation for structure in active_contents]
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
        new_space = ContextualSpace(
            structure_id=ID.new(ContextualSpace),
            parent_id=parent_id,
            name=self.name,
            parent_concept=self.parent_concept,
            contents=bubble_chamber.new_structure_collection(),
            conceptual_spaces=self.conceptual_spaces,
            links_in=bubble_chamber.new_structure_collection(),
            links_out=bubble_chamber.new_structure_collection(),
            parent_spaces=bubble_chamber.new_structure_collection(),
        )
        bubble_chamber.logger.log(new_space)
        copies = {}
        for item in self.contents.where(is_node=True):
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
                )
                new_item.links_in.add(new_relation)
                new_space.add(new_relation)
                copies[relation] = new_relation
        return new_space, copies
