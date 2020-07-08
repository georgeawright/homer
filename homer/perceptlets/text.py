from typing import List

from homer.perceptlet import Perceptlet
from homer.perceptlets.sentence import Sentence
from homer.perceptlets.relation import Relation


class Text(Perceptlet):
    """A piece of text made out of sentences and relations between them."""

    def __init__(
        self,
        text: str,
        sentences: List[Sentence],
        relations: List[Relation],
        strength: float,
    ):
        neighbours = []
        value = text
        Perceptlet.__init__(value, neighbours)
        self.sentences = sentences
        self.relations = relations
        self.strength = strength
