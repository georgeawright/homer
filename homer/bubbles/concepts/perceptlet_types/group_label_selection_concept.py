import random

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Concept
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelets.selectors import GroupLabelSelector
from homer.errors import MissingPerceptletError
from homer.workspace_location import WorkspaceLocation


class GroupLabelSelectionConcept(PerceptletType):
    def __init__(self, name: str = "group-label-selection"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber):
        if self.activation.as_scalar() > random.random():
            try:
                location = self.activation.get_high_location()
            except ValueError:
                return None
            try:
                target_group = bubble_chamber.workspace.groups.at(location).get_active()
            except MissingPerceptletError:
                return None
            return GroupLabelSelector(
                bubble_chamber,
                self,
                bubble_chamber.concept_space["group-label"],
                target_group,
                self.activation.at(location),
                self.concept_id,
            )

    def spawn_top_down_codelet(
        self,
        bubble_chamber: BubbleChamber,
        location: WorkspaceLocation,
        parent_concept: Concept,
    ):
        raise NotImplementedError
