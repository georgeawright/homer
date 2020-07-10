from homer.concept import Concept
from homer.perceptlet import Perceptlet


class Word(Perceptlet):
    """A word for use in text."""

    def __init__(self, text: str, parent_concept: Concept, strength: float):
        neighbours = []
        Perceptlet.__init__(self, text, neighbours)
        self.parent_concept = parent_concept
        self.strength = strength
