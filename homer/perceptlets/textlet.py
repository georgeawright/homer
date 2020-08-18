from __future__ import annotations

import statistics
from typing import List, Optional

from homer.concept import Concept
from homer.template import Template
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet
from homer.perceptlets.word import Word
from homer.perceptlet_collection import PerceptletCollection


class Textlet(Perceptlet):
    """A fragment of text."""

    IMPORTANCE_SIZE_WEIGHT = HyperParameters.TEXTLET_IMPORTANCE_SIZE_WEIGHT
    IMPORTANCE_CONSTITUENT_WEIGHT = (
        HyperParameters.TEXTLET_IMPORTANCE_CONSTITUENT_WEIGHT
    )
    IMPORTANCE_LABEL_WEIGHT = HyperParameters.TEXTLET_IMPORTANCE_LABEL_WEIGHT
    IMPORTANCE_STRENGTH_WEIGHT = HyperParameters.TEXTLET_IMPORTANCE_STRENGTH_WEIGHT

    def __init__(
        self,
        value: str,
        parent_template: Template,
        parent_concept: Concept,
        constituents: List[Word],
        constituent_relations: PerceptletCollection,
        strength: float,
        parent_id: str,
    ):
        location = None
        neighbours = PerceptletCollection()
        Perceptlet.__init__(self, value, location, neighbours, parent_id)
        self.parent_template = parent_template
        self.parent_concept = parent_concept
        self.constituents = (
            constituents if constituents is not None else PerceptletCollection()
        )
        self.constituent_relations = (
            constituent_relations
            if constituent_relations is not None
            else PerceptletCollection()
        )
        self.strength = strength
        self.relations = PerceptletCollection()

    def __str__(self) -> str:
        return " ".join([word.value for word in self.constituents])

    @property
    def size(self) -> int:
        return sum(constituent.size for constituent in self.constituents)

    @property
    def importance(self) -> float:
        return statistics.fmean(
            [
                self._size_based_importance * self.IMPORTANCE_SIZE_WEIGHT,
                self._constituent_based_importance * self.IMPORTANCE_CONSTITUENT_WEIGHT,
                self._label_based_importance * self.IMPORTANCE_LABEL_WEIGHT,
                self.strength * self.IMPORTANCE_STRENGTH_WEIGHT,
            ]
        )

    @property
    def _size_based_importance(self) -> float:
        return 1.0 - 1.0 / self.size

    @property
    def _constituent_based_importance(self) -> float:
        return max(constituent.importance for constituent in self.constituents)

    @property
    def unhappiness(self) -> float:
        connections = PerceptletCollection.union(self.labels, self.relations)
        return self._unhappiness_based_on_connections(connections)
