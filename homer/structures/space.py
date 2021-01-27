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
        self.parent_concept = parent_concept
        self.contents = contents
        self.no_of_dimensions = no_of_dimensions
        self._dimensions = dimensions
        self.sub_spaces = sub_spaces
        self.is_basic_level = is_basic_level
        self.super_space_to_coordinate_function_map = (
            (super_space_to_coordinate_function_map)
            if super_space_to_coordinate_function_map is not None
            else {}
        )

    @property
    def dimensions(self) -> List[Space]:
        if self.no_of_dimensions < 1:
            return []
        if self.no_of_dimensions == 1:
            return [self]
        return self._dimensions

    def add(self, structure: Structure):
        self.contents.add(structure)
        location_in_this_space = structure.location_in_space(self)
        for sub_space in self.sub_spaces:
            location_in_sub_space = sub_space.location_from_super_space_location(
                location_in_this_space
            )
            structure.locations.append(location_in_sub_space)
            sub_space.add(structure)
            structure.parent_spaces.add(sub_space)

    def is_compatible_with(self, other: Space) -> bool:
        return self.parent_concept.is_compatible_with(other.parent_concept)

    def get_relevant_value(self, chunk) -> Any:
        relevant_value = getattr(chunk, self.parent_concept.relevant_value)
        if self.coordinates_from_super_space_location is not None:
            relevant_value = self.coordinates_from_super_space_location(
                Location(relevant_value, None)
            )
        return relevant_value

    def location_from_super_space_location(self, location: Location) -> Location:
        coordinates_function = self.super_space_to_coordinate_function_map[
            location.space.name
        ]
        coordinates = coordinates_function(location)
        return Location(coordinates, self)

    def distance_between(self, a: Structure, b: Structure):
        return self.parent_concept.distance_between(a, b)

    def proximity_between(self, a: Structure, b: Structure):
        return self.parent_concept.proximity_between(a, b)
