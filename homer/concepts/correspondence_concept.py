from typing import Callable, List, Optional, Union

from homer.activation_patterns.workspace_activation_pattern import (
    WorkspaceActivationPattern,
)
from homer.concept import Concept


class CorrespondenceConcept(Concept):
    def __init__(
        self,
        name: str,
        affinity_calculation: Callable,
        depth: int = 1,
        activation: float = 0.0,
        space: Optional[Concept] = None,
        prototype: Optional[Union[List[int], List[float], str]] = None,
        boundary: Optional[Union[List[int], List[float]]] = None,
        distance_metric: Optional[Callable] = None,
    ):
        activation_coefficient = 1 / depth
        activation_pattern = WorkspaceActivationPattern(activation_coefficient)
        Concept.__init__(
            self,
            name,
            activation_pattern,
            depth=depth,
            space=space,
            prototype=prototype,
            boundary=boundary,
            distance_metric=distance_metric,
        )
        self.affinity_calculation = affinity_calculation

    def calculate_affinity(self, number_of_same_labels: int, proximity: float):
        raw_affinity = self.affinity_calculation(number_of_same_labels, proximity)
        return max(min(raw_affinity, 1.0), 0.0)
