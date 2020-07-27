from __future__ import annotations
from typing import List, Set

from homer.perceptlet import Perceptlet
from homer.perceptlets.raw_perceptlet import RawPerceptlet


class RawPerceptletField(Perceptlet):
    """A collection of raw perceptlets perceived at a single point in time"""

    def __init__(
        self,
        value: List[List[RawPerceptlet]],
        time: int,
        neighbours: Set[RawPerceptletField],
    ):
        location = None
        Perceptlet.__init__(value, location, time, neighbours)
