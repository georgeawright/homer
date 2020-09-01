import random

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Concept
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelets.evaluators import GroupEvaluator
from homer.errors import MissingPerceptletError
from homer.workspace_location import WorkspaceLocation


class GroupEvaluationConcept(PerceptletType):
    def __init__(self, name: str = "group-evaluation"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber) -> GroupEvaluator:
        if self.activation.as_scalar() > random.random():
            try:
                location = self.activation.get_high_location()
            except ValueError:
                return None
            try:
                target = bubble_chamber.workspace.groups.at(location).get_active()
            except MissingPerceptletError:
                return None
            return GroupEvaluator(
                bubble_chamber,
                self,
                bubble_chamber.concept_space.get_perceptlet_type_by_name("group"),
                target,
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
