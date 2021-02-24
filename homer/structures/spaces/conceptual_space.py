from __future__ import annotations

from typing import Callable, Dict, List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.nodes import Concept

from .working_space import WorkingSpace


class ConceptualSpace(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        locations: List[Location],
        contents: StructureCollection,
        no_of_dimensions: int,
        dimensions: List[ConceptualSpace],
        sub_spaces: List[ConceptualSpace],
        is_basic_level: bool = False,
        super_space_to_coordinate_function_map: Dict[str, Callable] = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        quality = 1
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
        self._instance = None
        self._instances = {}

    def instance_in_space(
        self, containing_space: Space, name: str = None
    ) -> WorkingSpace:
        if containing_space not in self._instances:
            locations = (
                [Location([], containing_space)] if containing_space is not None else []
            )
            dimensions = (
                [
                    dimension.instance_in_space(containing_space)
                    for dimension in self.dimensions
                ]
                if self.no_of_dimensions > 1
                else []
            )
            sub_spaces = [
                sub_space.instance_in_space(containing_space)
                for sub_space in self.sub_spaces
            ]
            self._instances[containing_space] = WorkingSpace(
                ID.new(WorkingSpace),
                "",
                self.name + " IN " + containing_space.name if name is None else name,
                self.parent_concept,
                self,
                locations,
                StructureCollection(),
                self.no_of_dimensions,
                dimensions,
                sub_spaces,
                is_basic_level=self.is_basic_level,
                super_space_to_coordinate_function_map=self.super_space_to_coordinate_function_map,
                links_in=StructureCollection(),
                links_out=StructureCollection(),
            )
        return self._instances[containing_space]

    def update_activation(self):
        if len(self.contents) == 0:
            self._activation = 0
        else:
            self._activation = max(item.activation for item in self.contents)
