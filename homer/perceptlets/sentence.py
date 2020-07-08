from typing import List

from homer.perceptlet import Perceptlet
from homer.perceptlets.phrase import Phrase
from homer.perceptlets.relation import Relation


class Sentence(Perceptlet):
    """A fragment of text made out of phrases and relations between them."""

    def __init__(
        self,
        text: str,
        phrases: List[Phrase],
        relations: List[Relation],
        strength: float,
    ):
        neighbours = []
        value = text
        Perceptlet.__init__(value, neighbours)
        self.phrases = phrases
        self.relations = relations
        self.strength = strength
