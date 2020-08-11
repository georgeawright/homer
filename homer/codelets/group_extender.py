from typing import Optional

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concepts.perceptlet_type import PerceptletType
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet

from homer.perceptlets.group import Group


class GroupExtender(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_group: Group,
        urgency: float,
        parent_id: str,
    ):
        Codelet.__init__(self, bubble_chamber, parent_id)
        self.perceptlet_type = perceptlet_type
        self.target_group = target_group
        self.urgency = urgency

    def run(self) -> Optional[Codelet]:
        neighbour = self.target_group.get_random_neighbour()
        confidence_of_group_membership = self._calculate_confidence(neighbour)
        if confidence_of_group_membership > self.CONFIDENCE_THRESHOLD:
            self.perceptlet_type.boost_activation(
                confidence_of_group_membership, self.target_group.location
            )
            self.target_group.add_member(neighbour)
            neighbour.add_group(self.target_group)
            print(
                f"GROUP EXTENDED: {self.target_group.value} at {self.target_group.location} and {neighbour.value} at {neighbour.location}, confidence: {confidence_of_group_membership}"
            )
        else:
            self.perceptlet_type.decay_activation([])
        return self.engender_follow_up(confidence_of_group_membership)

    def _calculate_confidence(self, candidate: Perceptlet) -> float:
        common_concepts = set.intersection(
            {label.parent_concept for label in candidate.labels},
            {label.parent_concept for label in self.target_group.labels},
        )
        distances = [
            concept.proximity_between(
                candidate.get_value(concept), self.target_group.get_value(concept)
            )
            for concept in common_concepts
        ]
        if distances == []:
            return 0.0
        return fuzzy.OR(*distances)

    def engender_follow_up(self, urgency: float):
        return GroupExtender(
            self.bubble_chamber,
            self.perceptlet_type,
            self.target_group,
            urgency,
            self.codelet_id,
        )
