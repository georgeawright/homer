from typing import List

from homer.perceptlet import Perceptlet
from homer.perceptlets.relation import Relation
from homer.perceptlets.word import Word


class Phrase(Perceptlet):
    """A fragement of text made out of words and relations between them."""

    def __init__(
        self, text: str, words: List[Word], relations: List[Relation], strength: float,
    ):
        neighbours = []
        value = text
        Perceptlet.__init__(self, value, neighbours)
        self.words = words
        self.relations = relations
        self.strength = strength
