from __future__ import annotations
import statistics
import random
from typing import Any, List, Set

from homer.errors import MissingPerceptletError
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet
from homer.perceptlets.relation import Relation


class Group(Perceptlet):
    """A grouping of other perceptlets."""

    IMPORTANCE_SIZE_WEIGHT = HyperParameters.GROUP_IMPORTANCE_SIZE_WEIGHT
    IMPORTANCE_LABEL_WEIGHT = HyperParameters.GROUP_IMPORTANCE_LABEL_WEIGHT
    IMPORTANCE_STRENGTH_WEIGHT = HyperParameters.GROUP_IMPORTANCE_STRENGTH_WEIGHT

    def __init__(
        self,
        value: Any,
        location: List[float],
        neighbours: Set[Perceptlet],
        members: Set[Perceptlet],
        strength: float,
        parent_id: str,
    ):
        Perceptlet.__init__(self, value, location, neighbours, parent_id)
        self.members = members
        self.strength = strength
        self.groups = set()
        self.relations = set()

    @property
    def size(self) -> int:
        return sum(member.size for member in self.members)

    @property
    def importance(self) -> float:
        return statistics.fmean(
            [
                self._size_based_importance * self.IMPORTANCE_SIZE_WEIGHT,
                self._label_based_importance * self.IMPORTANCE_LABEL_WEIGHT,
                self.strength * self.IMPORTANCE_STRENGTH_WEIGHT,
            ]
        )

    @property
    def _size_based_importance(self) -> float:
        return 1.0 - 1.0 / self.size

    @property
    def unhappiness(self) -> float:
        connections = self.labels | self.groups | self.relations
        return self._unhappiness_based_on_connections(connections)

    def get_random_member(self) -> Perceptlet:
        return random.sample(self.members, 1)[0]

    def add_member(self, new_member: Perceptlet):
        if type(self.value) != str:
            self.value = [
                (self.value[i] * self.size + new_member.value[i])
                / (self.size + new_member.size)
                for i in range(len(self.value))
            ]
        self.members.add(new_member)
        try:
            self.remove_neighbour(new_member)
        except KeyError:
            pass
        for new_neighbour in new_member.neighbours:
            if new_neighbour not in self.members:
                self.add_neighbour(new_neighbour)

    def get_random_label(self):
        if len(self.labels) < 1:
            raise MissingPerceptletError("Group has no labels")
        return random.sample(self.labels, 1)[0]

    def add_group(self, group: Group):
        self.groups.add(group)

    def add_relation(self, relation: Relation):
        self.relations.add(relation)
