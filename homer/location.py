from __future__ import annotations
import statistics
from typing import List


class Location:
    def __init__(self, x: float, y: float, space: "Space"):
        self.x = x
        self.y = y
        self.space = space

    @classmethod
    def average(cls, locations: List[Location]) -> Location:
        from .structures import Space

        return Location(
            statistics.fmean([location.x for location in locations]),
            statistics.fmean([location.y for location in locations]),
            locations[0].space,
        )
