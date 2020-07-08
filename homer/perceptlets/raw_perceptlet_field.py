from __future__ import annotations
from typing import List

from homer.perceptlet import Perceptlet
from homer.perceptlets.raw_perceptlet import RawPerceptlet


class RawPerceptletField(Perceptlet):
    """A collection of raw perceptlets perceived at a single point in time"""

    def __init__(
        self, value: List[List[RawPerceptlet]], neighbours: List[RawPerceptletField]
    ):
        Perceptlet.__init__(value, neighbours)
