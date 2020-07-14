from typing import List

from homer.perceptlet import Perceptlet
from homer.perceptlets.relation import Relation
from homer.perceptlets.word import Word


class Phrase(Perceptlet):
    """A fragment of text made out of words and relations between them."""

    def __init__(
        self,
        text: str,
        words: List[Word],
        internal_relations: List[Relation],
        strength: float,
    ):
        neighbours = []
        value = text
        Perceptlet.__init__(self, value, neighbours)
        self.words = words
        self.internal_relations = internal_relations
        self.strength = strength
        self.relations = set()

    @property
    def importance(self) -> float:
        return max(word.importance for word in self.words)

    @property
    def unhappiness(self) -> float:
        return self._unhappiness_based_on_connections(self.relations)

    def add_relation(self, relation: Relation):
        self.relations.add(relation)
