from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Concept
from homer.strategy import Strategy


class TopDown(Strategy):
    def __init__(self, bubble_chamber: BubbleChamber, concept: Concept = None):
        Strategy.__init__(self, bubble_chamber)
        self.concept = concept

    def concept(self, child_perceptlet_type: type):
        return self.bubble_chamber.concept_space.concepts_for_type(
            child_perceptlet_type
        ).get_active()
