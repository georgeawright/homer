import random

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Concept
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelets.evaluators import GroupLabelEvaluator
from homer.errors import MissingPerceptletError
from homer.workspace_location import WorkspaceLocation


class GroupLabelEvaluationConcept(PerceptletType):
    def __init__(self, name: str = "group-label-evaluation"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber) -> GroupLabelEvaluator:
        if self.activation.as_scalar() > random.random():
            try:
                location = self.activation.get_high_location()
            except ValueError:
                return None
            try:
                group = bubble_chamber.workspace.groups.at(location).get_active()
                target_label = group.labels.get_active()
            except MissingPerceptletError:
                return None
            return GroupLabelEvaluator(
                bubble_chamber,
                self,
                bubble_chamber.concept_space.get_perceptlet_type_by_name("group-label"),
                target_label,
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
