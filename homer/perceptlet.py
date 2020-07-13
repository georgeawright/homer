from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List

from homer.concept import Concept


class Perceptlet(ABC):
    """Any unit of perception."""

    def __init__(self, value: Any, neighbours: List[Any]):
        self.value = value
        self.neighbours = neighbours
        self.labels = set()

    @property
    def exigency(self):
        return self.importance * self.unhappiness

    @property
    def importance(self):
        raise NotImplementedError

    @property
    def unhappiness(self):
        raise NotImplementedError

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
