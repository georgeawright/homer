from __future__ import annotations
from typing import Optional

from homer.activation_patterns import PerceptletActivationPattern
from homer.bubbles.concept import Concept
from homer.bubbles.perceptlet import Perceptlet
from homer.perceptlet_collection import PerceptletCollection


class Word(Perceptlet):
    """A word for use in text."""

    def __init__(
        self,
        value: str,
        parent_concept: Optional[Concept],
        activation: PerceptletActivationPattern,
        parent_id: str,
    ):
        location = None
        neighbours = PerceptletCollection()
        Perceptlet.__init__(self, value, location, activation, neighbours, parent_id)
        self.parent_concept = parent_concept
        self.relations = PerceptletCollection()

    @classmethod
    def from_concept(cls, concept: Concept) -> Word:
        return cls(concept.name, concept, PerceptletActivationPattern(0.0), "")

    @classmethod
    def from_string(cls, word: str) -> Word:
        return cls(word, None, PerceptletActivationPattern(0.0), "")
