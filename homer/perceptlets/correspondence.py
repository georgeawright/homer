from __future__ import annotations

import statistics

from homer.concept import Concept
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet


class Correspondence(Perceptlet):
    """A perceived relationship between two perceptlets."""

    IMPORTANCE_LABEL_WEIGHT = HyperParameters.CORRESPONDENCE_IMPORTANCE_LABEL_WEIGHT
    IMPORTANCE_STRENGTH_WEIGHT = (
        HyperParameters.CORRESPONDENCE_IMPORTANCE_STRENGTH_WEIGHT
    )

    def __init__(
        self,
        name: str,
        parent_concept: Concept,
        first_argument: Perceptlet,
        second_argument: Perceptlet,
        strength: float,
        parent_id: str,
    ):
        location = first_argument.location
        neighbours = set()
        Perceptlet.__init__(self, name, location, neighbours, parent_id)
        self.parent_concept = parent_concept
        self.first_argument = first_argument
        self.second_argument = second_argument
        self.strength = strength
        self.correpsondences = set()

    @property
    def importance(self) -> float:
        return statistics.fmean(
            [
                self._label_based_importance * self.IMPORTANCE_LABEL_WEIGHT,
                self.strength * self.IMPORTANCE_STRENGTH_WEIGHT,
            ]
        )

    @property
    def unhappiness(self) -> float:
        # TODO: this might not be an appropriate measure of unhappiness for relations
        return self._unhappiness_based_on_connections(self.correspondences)

    def add_correspondence(self, correspondence: Correspondence):
        self.correspondences.add(correspondence)

    def is_between(self, a: Perceptlet, b: Perceptlet):
        return (self.first_argument == a and self.second_argument == b) or (
            self.first_argument == b and self.second_argument == a
        )
