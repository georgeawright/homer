import random

from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concept import Concept
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelets.correspondence_labeler import CorrespondenceLabeler
from homer.errors import MissingPerceptletError
from homer.workspace_location import WorkspaceLocation


class CorrespondenceLabelConcept(PerceptletType):
    def __init__(self, name: str = "correspondence-label"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber):
        if self.activation.as_scalar() > random.random():
            target_conceptual_space = bubble_chamber.get_random_conceptual_space()
            try:
                target_correspondence = (
                    bubble_chamber.workspace.correspondences.get_random()
                )
            except MissingPerceptletError:
                return None
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
