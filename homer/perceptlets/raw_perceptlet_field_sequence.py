from typing import List

from homer.perceptlet import Perceptlet
from homer.perceptlets.raw_perceptlet_field import RawPerceptletField


class RawPerceptletFieldSequence(Perceptlet):
    """A sequence of raw temporal data."""

    def __init__(self, value: List[RawPerceptletField]):
        location = None
        neighbours = set()
        Perceptlet.__init__(self, value, location, neighbours, "")

    def __iter__(self):
        return RawPerceptletFieldSequenceIterator(self)


class RawPerceptletFieldSequenceIterator:
    def __init__(self, sequence: RawPerceptletFieldSequence):
        self.sequence = sequence
        self._index = 0

    def __next__(self):
        if self._index >= len(self.sequence.value):
            raise StopIteration
        result = self.sequence.value[self._index]
        self._index += 1
        return result
