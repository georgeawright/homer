from __future__ import annotations
from abc import ABC

from .float_between_zero_and_one import FloatBetweenZeroAndOne
from .location import Location


class Structure(ABC):
    def __init__(self, location: Location, links_in: list, links_out: list):
        self.location = location
        self.links_in = links_in
        self.links_out = links_out
        self._activation = FloatBetweenZeroAndOne(0)
        self._unhappiness = FloatBetweenZeroAndOne(1)

    @property
    def exigency(self) -> FloatBetweenZeroAndOne:
        pass

    @property
    def activation(self) -> FloatBetweenZeroAndOne:
        return self._activation

    @property
    def unhappiness(self) -> FloatBetweenZeroAndOne:
        return self._unhappiness

    def boost_activation(self, amount: float = None):
        pass

    def decay_activation(self, amount: float = None):
        pass

    def add_link_in(self, link: Structure):
        pass

    def add_link_out(self, link: Structure):
        pass
