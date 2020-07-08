from abc import ABC
from typing import Any, List

from homer.concept import Concept


class Perceptlet(ABC):
    """Any unit of perception."""

    def __init__(self, value: Any, neighbours: List[Any]):
        self.value = value
        self.neighbours = neighbours
        self.labels = {}

    def proportion_of_neighbours_with_label(self, concept: Concept):
        pass

    def add_label(self, concept: Concept, strength: float):
        pass
