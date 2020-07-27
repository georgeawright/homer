from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.perceptlets.correspondence import Correspondence


class CorrespondenceLabeler(Codelet):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        target_correspondence: Correspondence,
        urgency: float,
    ):
        self.bubble_chamber = bubble_chamber
        self.target_correspondence = target_correspondence
        self.urgency = urgency

    def run(self):
        pass
