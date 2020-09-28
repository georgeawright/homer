from __future__ import annotations
from typing import Any, List

from homer.activation_patterns import PerceptletActivationPattern
from homer.bubbles.perceptlet import Perceptlet
from homer.perceptlet_collection import PerceptletCollection
from homer.perceptlet_collections import NeighbourCollection


class Group(Perceptlet):
    """A grouping of other perceptlets."""

    def __init__(
        self,
        value: Any,
        location: List[float],
        neighbours: NeighbourCollection,
        members: PerceptletCollection,
        activation: PerceptletActivationPattern,
        parent_id: str,
    ):
        Perceptlet.__init__(self, value, location, activation, neighbours, parent_id)
        self.members = members

    @property
    def size(self) -> int:
        return sum(member.size for member in self.members)

    def add_member(self, new_member: Perceptlet):
        if type(self.value) != str:
            self.value = [
                (self.value[i] * self.size + new_member.value[i])
                / (self.size + new_member.size)
                for i in range(len(self.value))
            ]
        self.members.add(new_member)
        try:
            self.neighbours.remove(new_member)
        except KeyError:
            pass
        for new_neighbour in new_member.neighbours:
            if new_neighbour not in self.members:
                self.neighbours.add(new_neighbour)
