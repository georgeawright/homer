from homer.bubble_chamber import BubbleChamber
from homer.strategy import Strategy


class BottomUp(Strategy):
    def __init__(self, bubble_chamber: BubbleChamber):
        Strategy.__init__(self, bubble_chamber)

    def concept(self, child_perceptlet_type: type):
        return self.bubble_chamber.concept_space.concepts_for_type(
            child_perceptlet_type
        ).get_random()
