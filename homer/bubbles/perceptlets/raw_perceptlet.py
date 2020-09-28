from __future__ import annotations
from typing import List, Union

from homer.activation_patterns import PerceptletActivationPattern
from homer.bubbles.perceptlet import Perceptlet
from homer.perceptlet_collections import NeighbourCollection


class RawPerceptlet(Perceptlet):
    """A single piece of perceived raw data, ie a number or symbol"""

    def __init__(
        self,
        value: Union[str, int, float],
        location: List[int],
        neighbours: NeighbourCollection,
    ):
        activation = PerceptletActivationPattern()
        Perceptlet.__init__(self, value, location, activation, neighbours, "")
