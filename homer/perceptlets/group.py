from __future__ import annotations
import statistics
from typing import Any, List

from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet
from homer.perceptlet_collection import PerceptletCollection


class Group(Perceptlet):
    """A grouping of other perceptlets."""

    IMPORTANCE_SIZE_WEIGHT = HyperParameters.GROUP_IMPORTANCE_SIZE_WEIGHT
    IMPORTANCE_LABEL_WEIGHT = HyperParameters.GROUP_IMPORTANCE_LABEL_WEIGHT
    IMPORTANCE_TEXTLET_WEIGHT = HyperParameters.GROUP_IMPORTANCE_TEXTLET_WEIGHT
    IMPORTANCE_STRENGTH_WEIGHT = HyperParameters.GROUP_IMPORTANCE_STRENGTH_WEIGHT

    def __init__(
        self,
        value: Any,
        location: List[float],
        neighbours: PerceptletCollection,
        members: PerceptletCollection,
        strength: float,
        parent_id: str,
    ):
        Perceptlet.__init__(self, value, location, neighbours, parent_id)
        self.members = members
        self.strength = strength
        self.groups = PerceptletCollection()
        self.correspondences = PerceptletCollection()
        self.textlets = PerceptletCollection()

    @property
    def size(self) -> int:
        return sum(member.size for member in self.members)

    @property
    def importance(self) -> float:
        return statistics.fmean(
            [
                self._size_based_importance * self.IMPORTANCE_SIZE_WEIGHT,
                self._label_based_importance * self.IMPORTANCE_LABEL_WEIGHT,
                self._textlet_based_importance * self.IMPORTANCE_TEXTLET_WEIGHT,
                self.strength * self.IMPORTANCE_STRENGTH_WEIGHT,
            ]
        )

    @property
    def _size_based_importance(self) -> float:
        return 1.0 - 1.0 / self.size

    @property
    def unhappiness(self) -> float:
        connections = PerceptletCollection.union(
            self.labels, self.groups, self.correspondences
        )
        return self._unhappiness_based_on_connections(connections)

    @property
    def _textlet_based_importance(self) -> float:
        total_textlet_strengths = sum(textlet.strength for textlet in self.textlets)
        total_textlet_strengths_inverse = 1.0 / (1.0 + total_textlet_strengths)
        return 1.0 - total_textlet_strengths_inverse

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
                self.add_neighbour(new_neighbour)

    def has_textlet(self, template, label):
        for textlet in self.textlets:
            if (
                textlet.parent_concept == label.parent_concept
                and textlet.parent_template == template
            ):
                return True
        return False
