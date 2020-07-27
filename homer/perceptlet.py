from __future__ import annotations
from abc import ABC
from typing import Any, List, Optional, Set, Union
import random
import statistics

from homer.concept import Concept
from homer.hyper_parameters import HyperParameters


class Perceptlet(ABC):
    """Any unit of perception."""

    IMPORTANCE_WEIGHT = HyperParameters.IMPORTANCE_WEIGHT
    UNHAPPINESS_WEIGHT = HyperParameters.UNHAPPINESS_WEIGHT

    def __init__(
        self,
        value: Any,
        location: Optional[List[Union[float, int]]],
        time: Optional[Union[float, int]],
        neighbours: Set[Perceptlet],
    ):
        self.value = value
        self.location = location
        self.time = time
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

    def get_value(self, concept: Concept) -> Any:
        return self.__getattr__(concept.relevant_value)

    def get_random_neighbour(self) -> Perceptlet:
        return random.choice(self.neighbours)

    def proportion_of_neighbours_with_label(self, concept: Concept) -> float:
        return self.number_of_neighbours_with_label(concept) / len(self.neighbours)

    def number_of_neighbours_with_label(self, concept: Concept) -> int:
        return sum(1 for neighbour in self.neighbours if neighbour.has_label(concept))

    def has_label(self, concept: Concept) -> bool:
        return True in (
            True for label in self.labels if label.parent_concept == concept
        )

    def labels_in_space(self, space: Concept) -> Set[Perceptlet]:
        return {label for label in self.labels if label.parent_concept.space == space}

    def has_label_in_space(self, space: Concept) -> bool:
        return len(self.labels_in_space(space)) > 0

    def add_label(self, label: Perceptlet) -> None:
        self.labels.add(label)

    def add_neighbour(self, neighbour: Perceptlet) -> None:
        self.neighbours.add(neighbour)

    def remove_neighbour(self, neighbour: Perceptlet) -> None:
        self.neighbours.remove(neighbour)
