from __future__ import annotations
from typing import List, Union

from homer.perceptlet import Perceptlet
from homer.perceptlet_collection import PerceptletCollection


class RawPerceptlet(Perceptlet):
    """A single piece of perceived raw data, ie a number or symbol"""

    def __init__(
        self,
        value: Union[str, int, float],
        location: List[int],
        neighbours: PerceptletCollection,
    ):
        Perceptlet.__init__(self, value, location, neighbours, "")
        self.groups = PerceptletCollection()
        self.relations = PerceptletCollection()

    @property
    def importance(self) -> float:
        return self._label_based_importance

    @property
    def unhappiness(self) -> float:
        connections = PerceptletCollection.union(
            self.labels, self.groups, self.relations
        )
        return self._unhappiness_based_on_connections(connections)
