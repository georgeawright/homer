import random

from homer.bubble_chamber import BubbleChamber
from homer.codelets.bottom_up_raw_perceptlet_labeler import BottomUpRawPerceptletLabeler
from homer.concepts.perceptlet_type import PerceptletType


class LabelConcept(PerceptletType):
    def __init__(self, name: str = "label"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber):
        activation = self.get_activation_as_scalar()
        if activation > random.random():
            target_perceptlet = bubble_chamber.get_raw_perceptlet()
            return BottomUpRawPerceptletLabeler(
                bubble_chamber, target_perceptlet, target_perceptlet.exigency
            )
