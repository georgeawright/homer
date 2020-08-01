from __future__ import annotations
from typing import List, Union, Set

from homer.perceptlet import Perceptlet
from homer.perceptlets.group import Group
from homer.perceptlets.relation import Relation


class RawPerceptlet(Perceptlet):
    """A single piece of perceived raw data, ie a number or symbol"""

    def __init__(
        self,
        value: Union[str, int, float],
        location: List[int],
        neighbours: Set[RawPerceptlet],
    ):
        Perceptlet.__init__(self, value, location, neighbours)
        self.groups = set()
        self.relations = set()

    @property
    def importance(self) -> float:
        return self._label_based_importance

    @property
    def unhappiness(self) -> float:
        connections = self.labels | self.groups | self.relations
        return self._unhappiness_based_on_connections(connections)

    def add_group(self, group: Group):
        self.groups.add(group)

    def add_relation(self, relation: Relation):
        self.relations.add(relation)
