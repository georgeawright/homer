import math
from typing import Optional

from homer.activation_patterns.workspace_activation_pattern import (
    WorkspaceActivationPattern,
)
from homer.concept import Concept


class EuclideanSpace(Concept):
    def __init__(
        self,
        name: str,
        depth: int,
        distance_to_proximity_weight: float,
        relevant_value: Optional[str] = "value",
    ):
        self.DISTANCE_TO_PROXIMITY_WEIGHT = distance_to_proximity_weight
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
