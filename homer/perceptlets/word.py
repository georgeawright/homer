import statistics

from homer.concept import Concept
from homer.perceptlet import Perceptlet
from homer.perceptlet_collection import PerceptletCollection


class Word(Perceptlet):
    """A word for use in text."""

    def __init__(
        self, text: str, parent_concept: Concept, strength: float, parent_id: str,
    ):
        location = None
        neighbours = PerceptletCollection()
        Perceptlet.__init__(self, text, location, neighbours, parent_id)
        self.parent_concept = parent_concept
        self.strength = strength
        self.relations = PerceptletCollection()

    @property
    def importance(self) -> float:
        return statistics.fmean([self.strength, self.parent_concept.activation])

    @property
    def unhappiness(self) -> float:
        return self._unhappiness_based_on_connections(self.relations)
