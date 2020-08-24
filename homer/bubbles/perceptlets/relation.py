from __future__ import annotations

import statistics

from homer.activation_patterns import PerceptletActivationPattern
from homer.bubbles import Concept, Perceptlet
from homer.perceptlet_collection import PerceptletCollection


class Relation(Perceptlet):
    """A perceived relationship between two perceptlets."""

    def __init__(
        self,
        name: str,
        parent_concept: Concept,
        first_argument: Perceptlet,
        second_argument: Perceptlet,
        activation: PerceptletActivationPattern,
        parent_id: str,
    ):
        location = None
        neighbours = PerceptletCollection()
        Perceptlet.__init__(self, name, location, activation, neighbours, parent_id)
        self.parent_concept = parent_concept
        self.first_argument = first_argument
        self.second_argument = second_argument
