from __future__ import annotations
from abc import ABC

from .float_between_one_and_zero import FloatBetweenOneAndZero
from .location import Location
from .structure_collection import StructureCollection


class Structure(ABC):
    def __init__(
        self,
        location: Location,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        self.location = location
        self._quality = quality
        self.links_in = StructureCollection() if links_in is None else links_in
        self.links_out = StructureCollection() if links_out is None else links_out
        self._activation = FloatBetweenOneAndZero(0)
        self._unhappiness = FloatBetweenOneAndZero(1)

    @property
    def exigency(self) -> FloatBetweenOneAndZero:
        pass

    @property
    def activation(self) -> FloatBetweenOneAndZero:
        return self._activation

    @property
    def quality(self) -> FloatBetweenOneAndZero:
        return self._quality

    @property
    def unhappiness(self) -> FloatBetweenOneAndZero:
        return self._unhappiness

    @property
    def labels(self) -> StructureCollection:
        from homer.structures.links import Label

        return StructureCollection(
            {link for link in self.links_out if isinstance(link, Label)}
        )

    @property
    def lexemes(self) -> StructureCollection:
        from homer.structures import Lexeme

        return StructureCollection(
            {link.end for link in self.links_out if isinstance(link.end, Lexeme)}
        )

    def has_relation(
        self, space: Structure, concept: Structure, second_argument: Structure
    ):
        pass

    def boost_activation(self, amount: float = None):
        pass

    def decay_activation(self, amount: float = None):
        pass

    def add_link_in(self, link: Structure):
        pass

    def add_link_out(self, link: Structure):
        pass
