from __future__ import annotations

import statistics

from homer.concept import Concept
from homer.perceptlet import Perceptlet


class Correspondence(Perceptlet):
    """A perceived relationship between two perceptlets."""

    def __init__(
        self,
        name: str,
        parent_concept: Concept,
        first_argument: Perceptlet,
        second_argument: Perceptlet,
        strength: float,
    ):
        location = None
        time = None
        neighbours = set()
        Perceptlet.__init__(self, name, location, time, neighbours)
        self.parent_concept = parent_concept
        self.first_argument = first_argument
        self.second_argument = second_argument
        self.strength = strength
        self.correpsondences = set()

    @property
    def importance(self) -> float:
        return statistics.fmean(
            [
                self._label_based_importance * self.LABEL_IMPORTANCE_WEIGHT,
                self.strength * self.STRENGTH_IMPORTANCE_WEIGHT,
            ]
        )

    @property
    def unhappiness(self) -> float:
        # TODO: this might not be an appropriate measure of unhappiness for relations
        return self._unhappiness_based_on_connections(self.relations)

    def add_relation(self, correspondence: Correspondence):
        self.correspondences.add(correspondence)
