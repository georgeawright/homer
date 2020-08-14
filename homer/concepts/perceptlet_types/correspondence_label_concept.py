import random

from homer.bubble_chamber import BubbleChamber
from homer.codelets.correspondence_labeler import CorrespondenceLabeler
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.workspace_location import WorkspaceLocation


class CorrespondenceLabelConcept(PerceptletType):
    def __init__(self, name: str = "correspondence-label"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber):
        activation = self.get_activation_as_scalar()
        if activation > random.random():
            target_conceptual_space = bubble_chamber.get_random_conceptual_space()
            target_correspondence = (
                bubble_chamber.workspace.correspondences.get_random()
            )
            return CorrespondenceLabeler(
                bubble_chamber,
                self,
                target_conceptual_space,
                target_correspondence,
                target_correspondence.exigency,
                self.concept_id,
            )

    def spawn_top_down_codelet(
        self,
        bubble_chamber: BubbleChamber,
        location: WorkspaceLocation,
        parent_concept: Concept,
    ):
        raise NotImplementedError
