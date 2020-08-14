from __future__ import annotations
import statistics
from abc import ABC
from typing import Any, List, Optional, Union

from homer.concept import Concept
from homer.hyper_parameters import HyperParameters
from homer.id import ID
from homer.perceptlet_collection import PerceptletCollection


class Perceptlet(ABC):
    """Any unit of perception."""

    IMPORTANCE_WEIGHT = HyperParameters.IMPORTANCE_WEIGHT
    UNHAPPINESS_WEIGHT = HyperParameters.UNHAPPINESS_WEIGHT

    def __init__(
        self,
        value: Any,
        location: Optional[List[Union[float, int]]],
        neighbours: PerceptletCollection,
        parent_id: str,
    ):
        self.value = value
        self.location = location
        self.perceptlet_id = ID.new(self)
        self.parent_id = parent_id
        self.neighbours = neighbours
        self.labels = PerceptletCollection()
        self.correspondences = PerceptletCollection()

    @property
    def size(self) -> int:
        return 1

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

    def _unhappiness_based_on_connections(
        self, connections: PerceptletCollection
    ) -> float:
        try:
            return 1.0 / len(connections)
        except ZeroDivisionError:
            return 1.0

    def get_value(self, concept: Concept) -> Any:
        return {
            "location": self.location[1:],
            "time": self.location[0],
            "value": self.value,
        }[concept.relevant_value]

    def proportion_of_neighbours_with_label(self, concept: Concept) -> float:
        return self.number_of_neighbours_with_label(concept) / len(self.neighbours)

    def number_of_neighbours_with_label(self, concept: Concept) -> int:
        return sum(1 for neighbour in self.neighbours if neighbour.has_label(concept))

    def has_label(self, concept: Concept) -> bool:
        return True in (
            True for label in self.labels if label.parent_concept == concept
        )

    def labels_in_space(self, space: Concept) -> PerceptletCollection:
        return PerceptletCollection(
            {label for label in self.labels if label.parent_concept.space == space}
        )

    def has_label_in_space(self, space: Concept) -> bool:
        return len(self.labels_in_space(space)) > 0

    def has_correspondence(self, second_perceptlet: Perceptlet, space: Concept) -> bool:
        for correspondence in self.correspondences:
            if (
                correspondence.is_between(self, second_perceptlet)
                and correspondence.parent_concept == space
            ):
                return True
        return False
