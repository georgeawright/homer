from __future__ import annotations
from typing import List

from .tools import average_vector


class Location:
    def __init__(self, coordinates: List[List[float]], space: "Space"):
        self.coordinates = coordinates
        self.space = space

    def __repr__(self):
        return f"({self.coordinates}, {self.space.name})"

    @classmethod
    def average(cls, locations: List[Location]) -> Location:
        return Location(
            [average_vector([location.coordinates[0] for location in locations])],
            locations[0].space,
        )

    @classmethod
    def merge(cls, location_one: Location, location_two: Location) -> Location:
        if location_one.coordinates[-1] != [location_two.coordinates[0][0] - 1]:
            raise Exception("locations are not adjacent")
        return Location(
            [location_one.coordinates[0], location_two.coordinates[-1]],
            location_one.space,
        )

    def __eq__(self, other: Location) -> bool:
        return self.coordinates == other.coordinates and self.space == other.space

    def __ne__(self, other: Location) -> bool:
        return not self == other

    def is_near(self, other: Location) -> bool:
        if self.space != other.space:
            return False
        distance = self.space.parent_concept.distance_function(
            self.coordinates, other.coordinates
        )
        return distance <= self.space.parent_concept.distance_to_proximity_weight
