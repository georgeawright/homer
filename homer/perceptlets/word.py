from __future__ import annotations
import statistics
from typing import Optional

from homer.concept import Concept
from homer.perceptlet import Perceptlet
from homer.perceptlet_collection import PerceptletCollection


class Word(Perceptlet):
    """A word for use in text."""

    def __init__(
        self,
        value: str,
        parent_concept: Optional[Concept],
        strength: float,
        parent_id: str,
    ):
        location = None
        neighbours = PerceptletCollection()
        Perceptlet.__init__(self, value, location, neighbours, parent_id)
        self.parent_concept = parent_concept
        self.strength = strength
        self.relations = PerceptletCollection()

    @classmethod
    def from_concept(cls, concept: Concept) -> Word:
        return cls(concept.name, concept, 0.0, "")

    @classmethod
    def from_string(cls, word: str) -> Word:
        return cls(word, None, 0.0, "")

    @property
    def importance(self) -> float:
        activation = (
            0.0
            if self.parent_concept is None
            else self.parent_concept.activation_pattern.get_activation_as_scalar()
        )
        return statistics.fmean([self.strength, activation])

    @property
    def unhappiness(self) -> float:
        return self._unhappiness_based_on_connections(self.relations)
