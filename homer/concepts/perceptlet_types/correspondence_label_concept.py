import random

from homer.bubble_chamber import BubbleChamber
from homer.codelets.correspondence_labeler import CorrespondenceLabeler
from homer.concepts.perceptlet_type import PerceptletType


class CorrespondenceLabelConcept(PerceptletType):
    def __init__(self, name: str = "correspondence-label"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber):
        activation = self.get_activation_as_scalar()
        if activation > random.random():
            target_correspondence = bubble_chamber.get_random_correspondence()
            return CorrespondenceLabeler(
                bubble_chamber,
                self,
                target_correspondence,
                target_correspondence.exigency,
            )
