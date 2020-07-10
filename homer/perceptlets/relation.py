from homer.concept import Concept
from homer.perceptlet import Perceptlet


class Relation(Perceptlet):
    """A perceived relationship between two perceptlets."""

    def __init__(
        self,
        name: str,
        parent_concept: Concept,
        first_argument: Perceptlet,
        second_argument: Perceptlet,
        strength: float,
    ):
        neighbours = []
        Perceptlet.__init__(self, name, neighbours)
        self.parent_concept = parent_concept
        self.first_argument = first_argument
        self.second_argument = second_argument
        self.strength = strength
