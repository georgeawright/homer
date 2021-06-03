from __future__ import annotations
from typing import List

from homer.location import Location


class TwoPointLocation(Location):
    def __init__(
        self,
        start_coordinates: List[List[float]],
        end_coordinates: List[List[float]],
        space: "Space",
    ):
        Location.__init__(self, start_coordinates, space)
        self.start_coordinates = start_coordinates
        self.end_coordinates = end_coordinates
        self.space = space

    def __repr__(self):
        return (
            f"({self.start_coordinates} to {self.end_coordinates}, {self.space.name})"
        )

    def __eq__(self, other: TwoPointLocation) -> bool:
        return (
            self.start_coordinates == other.start_coordinates
            and self.end_coordinates == other.end_coordinates
            and self.space == other.space
        )

    def __ne__(self, other: TwoPointLocation) -> bool:
        return not self == other

    def is_near(self, other: TwoPointLocation) -> bool:
        return self.start_is_near(other) and self.end_is_near(other)

    def start_is_near(self, other: Location) -> bool:
        if self.space != other.space:
            return False
        distance = self.space.parent_concept.distance_function(
            self.start_coordinates, other.start_coordinates
        )
        return distance <= self.space.parent_concept.distance_to_proximity_weight

    def end_is_near(self, other: Location) -> bool:
        if self.space != other.space:
            return False
        distance = self.space.parent_concept.distance_function(
            self.end_coordinates, other.end_coordinates
        )
        return distance <= self.space.parent_concept.distance_to_proximity_weight
