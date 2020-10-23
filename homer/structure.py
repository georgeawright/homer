from __future__ import annotations
from abc import ABC

from .float_between_zero_and_one import FloatBetweenZeroAndOne
from .location import Location


class Structure(ABC):
    def __init__(self, location: Location, links_in: list, conections_out: list):
        self.location = location
        self.links_in = links_in
        self.links_out = links_out
        self.activation = FloatBetweenZeroAndOne(0)

    def nearby(self):
        raise NotImplementedError
