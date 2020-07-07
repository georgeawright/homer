from abc import ABC

from homer.concept import Concept


class Perceptlet(ABC):
    def __init__(self):
        pass

    def proportion_of_neighbours_with_label(self, concept: Concept):
        pass

    def add_label(self, concept: Concept, strength: float):
        pass
