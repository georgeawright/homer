from typing import List, Union

from homer.activation_patterns import PerceptletActivationPattern
from homer.bubbles.concept import Concept
from homer.bubbles.perceptlet import Perceptlet
from homer.perceptlet_collections import NeighbourCollection


class Label(Perceptlet):
    """A label for any perceptlet."""

    def __init__(
        self,
        concept: Concept,
        location: List[Union[int, float]],
        target: Perceptlet,
        activation: PerceptletActivationPattern,
        parent_id,
    ):
        neighbours = NeighbourCollection()
        Perceptlet.__init__(
            self, concept.name, location, activation, neighbours, parent_id
        )
        self.parent_concept = concept
        self.target = target
