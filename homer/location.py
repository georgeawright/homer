from __future__ import annotations
import statistics
from typing import List


class Location:
    def __init__(self, coordinates: List[float], space: "Space"):
        self.coordinates = coordinates
        self.space = space

    @classmethod
    def average(cls, locations: List[Location]) -> Location:
        from .structures import Space

        return Location(
            [
                statistics.fmean([location.coordinates[i] for location in locations])
                for i in range(len(locations[0].coordinates))
            ],
            locations[0].space,
        )
