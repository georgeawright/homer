import random

from homer.bubble_chamber import BubbleChamber
from homer.codelets import GroupLabeler, TopDownGroupLabeler
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.errors import MissingPerceptletError
from homer.workspace_location import WorkspaceLocation


class GroupLabelConcept(PerceptletType):
    def __init__(self, name: str = "group-label"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber):
        activation = self.get_activation_as_scalar()
        if activation > random.random():
            target_group = bubble_chamber.workspace.groups.get_random()
            return GroupLabeler(
                bubble_chamber,
                self,
                target_group,
                target_group.exigency,
                self.concept_id,
            )

    def spawn_top_down_codelet(
        self,
        bubble_chamber: BubbleChamber,
        location: WorkspaceLocation,
        parent_concept: Concept,
    ):
        try:
            target_perceptlet = bubble_chamber.workspace.groups.at(
                location
            ).get_unhappy()
        except MissingPerceptletError:
            return None
        return TopDownGroupLabeler(
            bubble_chamber,
            self,
            parent_concept,
            target_perceptlet,
            target_perceptlet.exigency,
            parent_concept.concept_id,
        )
