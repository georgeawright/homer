from typing import List, Union

from homer.concept import Concept
from homer.perceptlet import Perceptlet
from homer.perceptlet_collection import PerceptletCollection


class Label(Perceptlet):
    """A label for any perceptlet."""

    def __init__(
        self,
        concept: Concept,
        location: List[Union[int, float]],
        strength: float,
        parent_id,
    ):
        neighbours = PerceptletCollection()
        Perceptlet.__init__(self, concept.name, location, neighbours, parent_id)
        self.parent_concept = concept
        self.strength = strength

    @property
    def importance(self) -> float:
        return 0.0

    @property
    def unhappiness(self) -> float:
        return 0.0
