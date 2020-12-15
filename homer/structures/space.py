from typing import Callable

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
        contents: list,
        quality: FloatBetweenOneAndZero,
        parent_concept: "Concept",
        parent_spaces: StructureCollection = None,
        child_spaces: StructureCollection = None,
        sub_spaces: StructureCollection = None,
        coordinates_from_super_space_location: Callable = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        location = None
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            location,
            quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.name = name
        self.value = name
        self.contents = contents
        self.parent_concept = parent_concept
        self.parent_spaces = (
            parent_spaces if parent_spaces is not None else StructureCollection()
        )
        self.child_spaces = (
            child_spaces if child_spaces is not None else StructureCollection()
        )
        self.sub_spaces = (
            sub_spaces if sub_spaces is not None else StructureCollection()
        )
        self.coordinates_from_super_space_location = (
            coordinates_from_super_space_location
        )

    def add(self, structure: Structure):
        self.contents.add(structure)
        if not hasattr(structure, "location_in_space"):
            return
        location_in_this_space = structure.location_in_space(self)
        for sub_space in self.sub_spaces:
            location_in_sub_space = sub_space.location_from_super_space_location(
                location_in_this_space
            )
            structure.locations.append(location_in_sub_space)
            sub_space.add(structure)
            structure.parent_spaces.add(sub_space)

    def location_from_super_space_location(self, location: Location) -> Location:
        if self.coordinates_from_super_space_location is None:
            raise Exception(
                f"{self.structure_id} has no coordinates-from-super-space-location function"
            )
        return Location(self.coordinates_from_super_space_location(location), self)

    def distance_between(self, a: Structure, b: Structure):
        return self.parent_concept.distance_between(a, b)

    def proximity_between(self, a: Structure, b: Structure):
        return self.parent_concept.proximity_between(a, b)
