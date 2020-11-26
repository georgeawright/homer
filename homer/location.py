from __future__ import annotations
import math
import statistics
from typing import List

from .hyper_parameters import HyperParameters
from .tools import average_vector


class Location:
    NEARNESS = HyperParameters.HOW_FAR_IS_NEAR

    def __init__(self, coordinates: List[float], space: "Space"):
        self.coordinates = coordinates
        self.space = space

    def __repr__(self):
        return f"({self.coordinates}, {self.space.name})"

    @classmethod
    def average(cls, locations: List[Location]) -> Location:
        from .structures import Space

        return Location(
            average_vector([location.coordinates for location in locations]),
            locations[0].space,
        )

    def __eq__(self, other: Location) -> bool:
        return self.coordinates == other.coordinates and self.space == other.space

    def __ne__(self, other: Location) -> bool:
        return not self == other

    def is_near(self, other: Location) -> bool:
        if self.space != other.space:
            return False
        return math.dist(self.coordinates, other.coordinates) <= self.NEARNESS
