import statistics
from typing import List, Set

from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet
from homer.perceptlets.phrase import Phrase
from homer.perceptlets.relation import Relation


class Sentence(Perceptlet):
    """A fragment of text made out of phrases and relations between them."""

    IMPORTANCE_SIZE_WEIGHT = HyperParameters.SENTENCE_IMPORTANCE_SIZE_WEIGHT
    IMPORTANCE_LABEL_WEIGHT = HyperParameters.SENTENCE_IMPORTANCE_LABEL_WEIGHT
    IMPORTANCE_STRENGTH_WEIGHT = HyperParameters.SENTENCE_IMPORTANCE_STRENGTH_WEIGHT

    def __init__(
        self,
        text: str,
        phrases: List[Phrase],
        internal_relations: Set[Relation],
        strength: float,
    ):
        neighbours = []
        value = text
        Perceptlet.__init__(self, value, neighbours)
        self.phrases = phrases
        self.internal_relations = internal_relations
        self.strength = strength
        self.relations = set()

    @property
    def size(self) -> int:
        return sum(phrase.size for phrase in self.phrases)

    @property
    def importance(self) -> float:
        return statistics.fmean(
            [
                self._size_based_importance * self.IMPORTANCE_SIZE_WEIGHT,
                self._label_based_importance * self.IMPORTANCE_LABEL_WEIGHT,
                self.strength * self.IMPORTANCE_STRENGTH_WEIGHT,
            ]
        )

    @property
    def _size_based_importance(self) -> float:
        return 1.0 - 1.0 / self.size

    @property
    def unhappiness(self) -> float:
        connections = self.labels | self.relations
        return self._unhappiness_based_on_connections(connections)

    def add_relation(self, relation: Relation):
        self.relations.add(relation)
