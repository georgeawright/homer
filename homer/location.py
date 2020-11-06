from __future__ import annotations
import statistics
from typing import List


class Location:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @classmethod
    def average(cls, locations: List[Location]) -> Location:
        return Location(
            statistics.fmean([location.x for location in locations]),
            statistics.fmean([location.y for location in locations]),
        )
