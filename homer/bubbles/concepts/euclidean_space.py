import math
import random
from typing import List, Optional

from homer.activation_patterns import WorkspaceActivationPattern
from homer.bubbles.concept import Concept
from homer.template import Template


class EuclideanSpace(Concept):
    def __init__(
        self,
        name: str,
        depth: int,
        distance_to_proximity_weight: float,
        templates: List[Template],
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
            relevant_value=relevant_value,
            distance_metric=distance_metric,
        )
        self.DISTANCE_TO_PROXIMITY_WEIGHT = distance_to_proximity_weight
        self.templates = templates

    def get_template(self):
        return random.choice(self.templates)
