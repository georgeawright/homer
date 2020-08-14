import math
from typing import List, Optional

from homer.activation_patterns.workspace_activation_pattern import (
    WorkspaceActivationPattern,
)
from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelets.group_labeler import GroupLabeler
from homer.codelets.raw_perceptlet_labeler import RawPerceptletLabeler
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
        self.DISTANCE_TO_PROXIMITY_WEIGHT = self.space.DISTANCE_TO_PROXIMITY_WEIGHT

    def spawn_codelet(self, bubble_chamber: BubbleChamber) -> Optional[Codelet]:
        if self.activation_pattern.is_high():
            location = self.activation_pattern.get_high_location()
            perceptlet_type = Concept.most_active(
                bubble_chamber.concept_space.get_perceptlet_type_by_name("label"),
                bubble_chamber.concept_space.get_perceptlet_type_by_name("group-label"),
                location=location,
            )
            return perceptlet_type.spawn_top_down_codelet(bubble_chamber, location)
