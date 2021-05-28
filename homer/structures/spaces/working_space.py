from __future__ import annotations

import statistics
from typing import Callable, Dict, List

from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Node, Space
from homer.structures.nodes import Concept


class WorkingSpace(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        conceptual_space: Space,
        locations: List[Location],
        contents: StructureCollection,
        no_of_dimensions: int,
        dimensions: List[WorkingSpace],
        sub_spaces: List[WorkingSpace],
        is_basic_level: bool = False,
        super_space_to_coordinate_function_map: Dict[str, Callable] = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        quality = 0
        Space.__init__(
            self,
            structure_id,
            parent_id,
            name,
            parent_concept,
            locations,
            contents,
            no_of_dimensions,
            dimensions,
            sub_spaces,
            quality,
            is_basic_level=is_basic_level,
            super_space_to_coordinate_function_map=super_space_to_coordinate_function_map,
            links_in=links_in,
            links_out=links_out,
        )
        self.conceptual_space = conceptual_space
        self.is_working_space = True

    @property
    def quality(self):
        active_contents = {
            structure
            for space in [self] + self.sub_spaces
            for structure in space.contents
            if structure.activation > 0
        }
        if len(active_contents) == 0:
            return 0.0
        return statistics.fmean(
            [structure.quality * structure.activation for structure in active_contents]
        )

    def copy(self, **kwargs: dict) -> WorkingSpace:
        """Requires keyword arguments 'bubble_chamber' and 'parent_id'."""
        from homer.structures.links import Relation

        bubble_chamber = kwargs["bubble_chamber"]
        parent_id = kwargs["parent_id"]
        sub_space_copies = {
            sub_space: sub_space.copy_without_contents for sub_space in self.sub_spaces
        }
        new_dimensions = [
            sub_space_copies[dimension]
            for dimension in self.dimensions
            if dimension != self
        ]
        new_sub_spaces = [sub_space_copies[sub_space] for sub_space in self.sub_spaces]
        new_space = WorkingSpace(
            structure_id=ID.new(WorkingSpace),
            parent_id=parent_id,
            name=self.name,
            parent_concept=self.parent_concept,
            conceptual_space=self.conceptual_space,
            locations=self.locations,
            contents=StructureCollection(),
            no_of_dimensions=self.no_of_dimensions,
            dimensions=new_dimensions,
            sub_spaces=new_sub_spaces,
            is_basic_level=self.is_basic_level,
            super_space_to_coordinate_function_map=self.super_space_to_coordinate_function_map,
        )
        bubble_chamber.logger.log(new_space)
        copies = {}
        for item in self.contents:
            if isinstance(item, Node):
                new_item = item.copy(
                    bubble_chamber=bubble_chamber,
                    parent_id=parent_id,
                    parent_space=new_space,
                )
                new_space.add(new_item)
                copies[item] = new_item
                for label in item.labels:
                    new_label = label.copy(
                        start=new_item,
                        parent_space=new_space,
                        parent_id=parent_id,
                    )
                    new_item.links_out.add(new_label)
                    new_space.add(new_label)
                for relation in item.links_out.of_type(Relation):
                    if relation.end not in copies:
                        continue
                    new_end = copies[relation.end]
                    new_relation = relation.copy(
                        start=new_item, end=new_end, parent_space=new_space
                    )
                    new_item.links_out.add(new_relation)
                    new_space.add(new_relation)
                for relation in item.links_in.of_type(Relation):
                    if relation.start not in copies:
                        continue
                    new_start = copies[relation.start]
                    new_relation = relation.copy(
                        start=new_start, end=new_item, parent_space=new_space
                    )
                    new_item.links_in.add(new_relation)
                    new_space.add(new_relation)
                for correspondence in item.correspondences:
                    new_correspondence = correspondence.copy(
                        old_arg=item, new_arg=new_item, parent_id=parent_id
                    )
                    new_correspondence.start.links_in.add(new_correspondence)
                    new_correspondence.start.links_out.add(new_correspondence)
                    new_correspondence.end.links_in.add(new_correspondence)
                    new_correspondence.end.links_out.add(new_correspondence)
                    new_space.add(new_correspondence)
        return new_space

    def copy_without_contents(
        self, parent_id: str, parent_space: WorkingSpace = None
    ) -> WorkingSpace:
        """Returns an empty working space with the same conceptual space."""
        parent_space = self.parent_space if parent_space is None else parent_space
        sub_space_copies = {
            sub_space: sub_space.copy_without_contents(
                parent_id, parent_space=parent_space
            )
            for sub_space in self.sub_spaces
        }
        new_dimensions = (
            [sub_space_copies[dimension] for dimension in self.dimensions]
            if self.no_of_dimensions > 1
            else []
        )
        new_sub_spaces = [sub_space_copies[sub_space] for sub_space in self.sub_spaces]
        locations = [
            Location(location.coordinates, parent_space)
            if location.space.conceptual_space == parent_space.conceptual_space
            else location
            for location in self.locations
        ]
        new_space = WorkingSpace(
            structure_id=ID.new(WorkingSpace),
            parent_id=parent_id,
            name=self.name,
            parent_concept=self.parent_concept,
            conceptual_space=self.conceptual_space,
            locations=locations,
            contents=StructureCollection(),
            no_of_dimensions=self.no_of_dimensions,
            dimensions=new_dimensions,
            sub_spaces=new_sub_spaces,
            is_basic_level=self.is_basic_level,
            super_space_to_coordinate_function_map=self.super_space_to_coordinate_function_map,
        )
        return new_space

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

    def location_from_super_space_location(self, location: Location) -> Location:
        space = (
            location.space.name
            if location.space.conceptual_space is None
            else location.space.conceptual_space.name
        )
        coordinates_function = self.super_space_to_coordinate_function_map[space]
        coordinates = coordinates_function(location)
        return Location(coordinates, self)
