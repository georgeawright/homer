from __future__ import annotations
from typing import Union

from homer.variable import Variable


class NumberVariable(Variable):
    def __init__(
        self,
        min_value: Union[float, NumberVariable] = float("-inf"),
        max_value: Union[float, NumberVariable] = float("inf"),
    ):
        self.min_value = min_value
        self.max_value = max_value

    def __lt__(self, other) -> bool:
        return self.max_value < other

    def __le__(self, other) -> bool:
        return self.max_value <= other

    def __gt__(self, other) -> bool:
        return self.min_value > other

    def __ge__(self, other) -> bool:
        return self.min_value >= other

    def subsumes(self, number) -> bool:
        return self.min_value <= number <= self.max_value
