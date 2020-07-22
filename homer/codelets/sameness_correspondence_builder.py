from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.hyper_parameters import HyperParameters
from homer.perceptlets.group import Group


class SamenessCorrespondenceBuilder(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        target_group_a: Group,
        target_group_b: Group,
    ):
        self.bubble_chamber = bubble_chamber
        self.target_group_a = target_group_a
        self.target_group_b = target_group_b

    def run(self) -> Optional[Codelet]:
        pass

    def _calculate_confidence(self) -> float:
        """Returns a high value for groups labeled with a proximate concept."""
        pass

    def _engender_follow_up(self, urgency: float) -> Codelet:
        pass
