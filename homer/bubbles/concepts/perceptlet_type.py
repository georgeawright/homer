from abc import abstractmethod

from homer.activation_patterns import WorkspaceActivationPattern
from homer.bubbles.concept import Concept
from homer.workspace_location import WorkspaceLocation


class PerceptletType(Concept):
    def __init__(self, name: str, depth: int = 1):
        activation_coefficient = 1 / depth
        activation_pattern = WorkspaceActivationPattern(activation_coefficient)
        Concept.__init__(
            self,
            name,
            activation_pattern,
            depth=depth,
        )

    @abstractmethod
    def spawn_codelet(self, bubble_chamber):
        pass

    @abstractmethod
    def spawn_top_down_codelet(
        self,
        bubble_chamber,
        location: WorkspaceLocation,
        parent_id: str,
    ):
        pass
