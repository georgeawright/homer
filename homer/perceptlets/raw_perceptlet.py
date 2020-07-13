from __future__ import annotations
from typing import List, Union

from homer.perceptlet import Perceptlet
from homer.perceptlets.group import Group
from homer.perceptlets.relation import Relation


class RawPerceptlet(Perceptlet):
    """A single piece of perceived raw data, ie a number or symbol"""

    def __init__(self, value: Union[str, int, float], neighbours: List[RawPerceptlet]):
        Perceptlet.__init__(self, value, neighbours)
        self.groups = set()
        self.relations = set()

    @property
    def importance(self) -> float:
        total_label_strengths = sum(label.strength for label in self.labels)
        total_label_strengths_inverse = 1.0 / (1.0 + total_label_strengths)
        return 1.0 - total_label_strengths_inverse

    @property
    def unhappiness(self) -> float:
        total_connections = len(self.labels) + len(self.relations) + len(self.groups)
        print(total_connections)
        try:
            return 1.0 / total_connections
        except ZeroDivisionError:
            return 1.0

    def add_group(self, group: Group):
        self.groups.add(group)

    def add_relation(self, relation: Relation):
        self.relations.add(relation)
