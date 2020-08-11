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
        Perceptlet.__init__(self, value, location, neighbours, "")
        self.time = time

    def __iter__(self):
        return RawPerceptletFieldIterator(self)


class RawPerceptletFieldIterator:
    def __init__(self, field: RawPerceptletField):
        self.field = field
        self._index = 0

    def __next__(self):
        if self._index >= len(self.field.value):
            raise StopIteration
        result = self.field.value[self._index]
        self._index += 1
        return result
