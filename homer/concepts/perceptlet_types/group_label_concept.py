import random

from homer.bubble_chamber import BubbleChamber
from homer.codelets.group_labeler import GroupLabeler
from homer.concepts.perceptlet_type import PerceptletType
from homer.workspace_location import WorkspaceLocation


class GroupLabelConcept(PerceptletType):
    def __init__(self, name: str = "group-label"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber):
        activation = self.get_activation_as_scalar()
        if activation > random.random():
            target_group = bubble_chamber.get_random_groups(1)[0]
            return GroupLabeler(
                bubble_chamber,
                self,
                target_group,
                target_group.exigency,
                self.concept_id,
            )

    def spawn_top_down_codelet(
        self, bubble_chamber: BubbleChamber, location: WorkspaceLocation, parent_id: str
    ):
        raise NotImplementedError
