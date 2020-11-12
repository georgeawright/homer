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
        self._activation_buffer = 0.0
        self._unhappiness = FloatBetweenOneAndZero(1)

    @property
    def coordinates(self) -> list:
        return self.location.coordinates

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

    def nearby(self, space: Structure = None):
        raise NotImplementedError

    def has_label(self, concept: Structure) -> bool:
        for link in self.links_out:
            if link.parent_concept == concept and link.end is None:
                return True
        return False

    def has_relation(
        self, space: Structure, concept: Structure, second_argument: Structure
    ) -> bool:
        for link in self.links_out:
            if (
                link.parent_concept == concept
                and link.end == second_argument
                and link.parent_space == space
            ):
                return True
        return False

    def has_correspondence(
        self, space: Structure, concept: Structure, second_argument: Structure
    ) -> bool:
        for link in self.links_out:
            if (
                link.parent_concept == concept
                and link.end == second_argument
                and link.parent_space == space
            ):
                return True
        return False

    def boost_activation(self, amount: float = None):
        self._activation_buffer += amount

    def decay_activation(self, amount: float = None):
        self._activation_buffer -= amount

    def update_activation(self):
        self._activation = FloatBetweenOneAndZero(
            self._activation + self._activation_buffer
        )
        self._activation_buffer = 0.0
