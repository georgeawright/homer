from typing import List

from homer.concept import Concept
from homer.perceptlet import Perceptlet


class Label(Perceptlet):
    """A label for any perceptlet."""

    def __init__(
        self, concept: Concept, location: List[int], strength: float, parent_id
    ):
        neighbours = set()
        Perceptlet.__init__(self, concept.name, location, neighbours, parent_id)
        self.parent_concept = concept
        self.strength = strength

    @property
    def importance(self) -> float:
        return 0.0

    @property
    def unhappiness(self) -> float:
        return 0.0
