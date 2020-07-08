from homer.concept import Concept
from homer.perceptlet import Perceptlet


class Word(Perceptlet):
    """A word for use in text."""

    def __init__(self, value: str, parent_concept: Concept, strength: float):
        neighbours = []
        Perceptlet.__init__(value, neighbours)
        self.parent_concept = parent_concept
        self.strength = strength
