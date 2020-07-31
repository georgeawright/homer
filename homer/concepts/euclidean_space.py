import math
from typing import Optional

from homer.activation_patterns.workspace_activation_pattern import (
    WorkspaceActivationPattern,
)
from homer.concept import Concept


class EuclideanSpace(Concept):
    def __init__(self, name: str, depth: int, relevant_value: Optional[str] = "value"):
        distance_metric = math.dist
        activation_coefficient = 1 / depth
        activation_pattern = WorkspaceActivationPattern(activation_coefficient)
        Concept.__init__(
            self,
            name,
            activation_pattern,
            depth=depth,
            relevant_value=relevant_value,
            distance_metric=distance_metric,
        )
