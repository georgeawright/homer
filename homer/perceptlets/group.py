from typing import List

from homer.perceptlet import Perceptlet


class Group(Perceptlet):
    """A grouping of other perceptlets."""

    def __init__(self, members: List[Perceptlet], strength: float):
        value = "?"
        neighbours = []
        Perceptlet.__init__(self, value, neighbours)
        self.members = members
        self.strength = strength
