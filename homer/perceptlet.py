from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List, Set
import statistics

from homer.concept import Concept
from homer.hyper_parameters import HyperParameters


class Perceptlet(ABC):
    """Any unit of perception."""

    IMPORTANCE_WEIGHT = HyperParameters.IMPORTANCE_WEIGHT
    UNHAPPINESS_WEIGHT = HyperParameters.UNHAPPINESS_WEIGHT

    def __init__(self, value: Any, neighbours: List[Any]):
        self.value = value
        self.neighbours = neighbours
        self.labels = set()

    @property
    def exigency(self) -> float:
        """Returns a rating between 0 and 1."""
        return statistics.fmean(
            [
                self.IMPORTANCE_WEIGHT * self.importance,
                self.UNHAPPINESS_WEIGHT * self.unhappiness,
            ]
        )

    @property
    def importance(self) -> float:
        """Returns a rating between 0 and 1."""
        raise NotImplementedError

    @property
    def unhappiness(self) -> float:
        """Returns a rating between 0 and 1."""
        raise NotImplementedError

    @property
    def _label_based_importance(self) -> float:
        total_label_strengths = sum(label.strength for label in self.labels)
        total_label_strengths_inverse = 1.0 / (1.0 + total_label_strengths)
        return 1.0 - total_label_strengths_inverse

    def _unhappiness_based_on_connections(self, connections: Set[Perceptlet]) -> float:
        try:
            return 1.0 / len(connections)
        except ZeroDivisionError:
            return 1.0

    def proportion_of_neighbours_with_label(self, concept: Concept) -> float:
        return self.number_of_neighbours_with_label(concept) / len(self.neighbours)

    def number_of_neighbours_with_label(self, concept: Concept) -> int:
        return sum(1 for neighbour in self.neighbours if neighbour.has_label(concept))

    def has_label(self, concept: Concept) -> bool:
        return True in (
            True for label in self.labels if label.parent_concept == concept
        )

    def add_label(self, label: Perceptlet) -> None:
        self.labels.add(label)
