from abc import abstractmethod
from homer.activation_patterns.workspace_activation_pattern import (
    WorkspaceActivationPattern,
)
from homer.concept import Concept
from homer.workspace_location import WorkspaceLocation


class PerceptletType(Concept):
    def __init__(self, name: str, depth: int = 1):
        activation_coefficient = 1 / depth
        activation_pattern = WorkspaceActivationPattern(activation_coefficient)
        Concept.__init__(
            self, name, activation_pattern, depth=depth,
        )

    @abstractmethod
    def spawn_top_down_codelet(self, location: WorkspaceLocation):
        pass
