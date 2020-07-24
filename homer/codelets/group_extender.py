from typing import Optional

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet

from homer.perceptlets.group import Group


class GroupExtender(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self, bubble_chamber: BubbleChamber, target_group: Group, urgency: float
    ):
        Codelet.__init__(self, bubble_chamber)
        self.target_group = target_group
        self.urgency = urgency

    def run(self) -> Optional[Codelet]:
        neighbour = self.target_group.get_random_neighbour()
        confidence_of_group_membership = self._calculate_confidence(neighbour)
        if confidence_of_group_membership > self.CONFIDENCE_THRESHOLD:
            self.group.add_member(neighbour)
            self.neighbour.add_group(self.target_group)
        return self.engender_follow_up(confidence_of_group_membership)

    def _calculate_confidence(self, candidate: Perceptlet) -> float:
        common_concepts = {
            label.parent_concept for label in candidate.labels
        }.intersection({label.parent_concept for label in self.target_group.labels})
        distances = [
            concept.proximity_between(candidate.value, self.target_group.value)
            for concept in common_concepts
        ]
        if distances == []:
            return 0.0
        return fuzzy.OR(*distances)

    def engender_follow_up(self, urgency: float):
        return GroupExtender(self.bubble_chamber, self.target_group, urgency)
