from __future__ import annotations

from typing import Any, Callable, Dict, List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection


class Space(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: "Concept",
        locations: List[Location],
        contents: StructureCollection,
        no_of_dimensions: int,
        dimensions: List[Space],
        sub_spaces: List[Space],
        quality: FloatBetweenOneAndZero,
        is_basic_level: bool = False,
        is_symbolic: bool = False,
        super_space_to_coordinate_function_map: Dict[str, Callable] = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            locations,
            quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.name = name
        self.value = name
        self._parent_concept = parent_concept
        self.contents = contents
        self.no_of_dimensions = no_of_dimensions
        self._dimensions = dimensions
        self.sub_spaces = sub_spaces
        self.is_basic_level = is_basic_level
        self.is_symbolic = is_symbolic
        self.super_space_to_coordinate_function_map = (
            (super_space_to_coordinate_function_map)
            if super_space_to_coordinate_function_map is not None
            else {}
        )
        self.is_space = True

    @property
    def dimensions(self) -> List[Space]:
        if self.no_of_dimensions < 1:
            return []
        if self.no_of_dimensions == 1:
            return [self]
        return self._dimensions

    def add(self, structure: Structure):
        location_in_this_space = structure.location_in_space(self)
        if structure not in self.contents:
            self.contents.add(structure)
            for sub_space in self.sub_spaces:
                location_in_sub_space = sub_space.location_from_super_space_location(
                    location_in_this_space
                )
                structure.locations.append(location_in_sub_space)
                sub_space.add(structure)

    def is_compatible_with(self, other: Space) -> bool:
        return self.parent_concept.is_compatible_with(other.parent_concept)

    def location_from_super_space_location(self, location: Location) -> Location:
        if location.coordinates[0][0] is None:
            coordinates = [[None for _ in range(self.no_of_dimensions)]]
        else:
            coordinates_function = self.super_space_to_coordinate_function_map[
                location.space.name
            ]
            coordinates = coordinates_function(location)
        return Location(coordinates, self)

    def distance_between(self, a: Structure, b: Structure):
        return self.parent_concept.distance_between(a, b, space=self)

    def proximity_between(self, a: Structure, b: Structure):
        return self.parent_concept.proximity_between(a, b, space=self)

    def __repr__(self) -> str:
        return f"<{self.structure_id} {self.name}>"
