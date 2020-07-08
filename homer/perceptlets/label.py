from homer.concept import Concept
from homer.perceptlet import Perceptlet


class Label(Perceptlet):
    """A label for any perceptlet."""

    def __init__(self, concept: Concept, strength: float):
        neighbours = []
        Perceptlet.__init__(concept.name, neighbours)
        self.parent_concept = concept
        self.strength = strength
