import math

from homer.activation_patterns.workspace_activation_pattern import (
    WorkspaceActivationPattern,
)
from homer.concept import Concept


class EuclideanSpace(Concept):
    def __init__(
        self, name: str, depth: int,
    ):
        distance_metric = math.dist
        activation_coefficient = 1 / depth
        activation_pattern = WorkspaceActivationPattern(activation_coefficient)
        Concept.__init__(
            self,
            name,
            activation_pattern,
            depth=depth,
            distance_metric=distance_metric,
        )
