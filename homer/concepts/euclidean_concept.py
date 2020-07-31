import math
from typing import List, Optional

from homer.activation_patterns.workspace_activation_pattern import (
    WorkspaceActivationPattern,
)
from homer.concept import Concept


class EuclideanConcept(Concept):
    def __init__(
        self,
        name: str,
        prototype: List[int],
        space: Concept,
        depth: int = 1,
        boundary: Optional[List[int]] = None,
        relevant_value: Optional[str] = "value",
    ):
        activation_coefficient = 1 / depth
        activation_pattern = WorkspaceActivationPattern(activation_coefficient)
        distance_metric = math.dist
        Concept.__init__(
            self,
            name,
            activation_pattern,
            depth=depth,
            space=space,
            prototype=prototype,
            boundary=boundary,
            relevant_value=relevant_value,
            distance_metric=distance_metric,
        )
