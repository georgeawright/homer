from __future__ import annotations

from typing import Callable, List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Space

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
        coordinates_from_super_space_location: Callable = None,
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
            coordinates_from_super_space_location=coordinates_from_super_space_location,
            links_in=links_in,
            links_out=links_out,
        )
        self._instance = None

    @property
    def instance(self) -> WorkingSpace:
        if self._instance is None:
            locations = [
                Location(location.coordinates, location.space.instance)
                for location in self.locations
            ]
            dimensions = (
                [dimension.instance for dimension in self.dimensions]
                if self.no_of_dimensions > 1
                else []
            )
            sub_spaces = [sub_space.instance for sub_space in self.sub_spaces]
            self._instance = WorkingSpace(
                self.structure_id + "_working_space",
                "",
                self.name + " working",
                self.parent_concept,
                locations,
                StructureCollection(),
                self.no_of_dimensions,
                dimensions,
                sub_spaces,
                is_basic_level=self.is_basic_level,
                coordinates_from_super_space_location=self.coordinates_from_super_space_location,
                links_in=StructureCollection(),
                links_out=StructureCollection(),
            )
        return self._instance

    def update_activation(self):
        self._activation = max(item.activation for item in self.contents)
