from __future__ import annotations
from typing import List

import statistics

from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet
from homer.perceptlets.relation import Relation


class Group(Perceptlet):
    """A grouping of other perceptlets."""

    SIZE_IMPORTANCE_WEIGHT = HyperParameters.SIZE_IMPORTANCE_WEIGHT
    LABEL_IMPORTANCE_WEIGHT = HyperParameters.LABEL_IMPORTANCE_WEIGHT

    def __init__(self, members: List[Perceptlet], strength: float):
        value = "?"
        neighbours = []
        Perceptlet.__init__(self, value, neighbours)
        self.members = members
        self.strength = strength
        self.groups = set()
        self.relations = set()

    @property
    def size(self) -> int:
        return sum(
            member.size if type(member) == Group else 1 for member in self.members
        )

    @property
    def importance(self) -> float:
        return statistics.fmean(
            [
                self._size_based_importance * self.SIZE_IMPORTANCE_WEIGHT,
                self._label_based_importance * self.LABEL_IMPORTANCE_WEIGHT,
                self.strength * self.STRENGTH_IMPORTANCE_WEIGHT,
            ]
        )

    @property
    def _size_based_importance(self) -> float:
        return 1.0 - 1.0 / self.size

    @property
    def unhappiness(self) -> float:
        connections = self.labels | self.groups | self.relations
        return self._unhappiness_based_on_connections(connections)

    def add_group(self, group: Group):
        self.groups.add(group)

    def add_relation(self, relation: Relation):
        self.relations.add(relation)
