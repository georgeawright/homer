import random
from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelets.group_extender import GroupExtender
from homer.concept import Concept
from homer.hyper_parameters import HyperParameters
from homer.perceptlets.group import Group


class GroupLabeler(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        target_group: Optional[Group],
        urgency: float,
    ):
        Codelet.__init__(self, bubble_chamber)
        self.target_group = target_group
        self.urgency = urgency

    def run(self) -> Optional[Codelet]:
        target_concept = self._get_target_label()
        confidence_of_class_affinity = self._calculate_confidence(target_concept)
        if confidence_of_class_affinity > self.CONFIDENCE_THRESHOLD:
            target_concept.boost_activation(
                confidence_of_class_affinity, self.target_group.location
            )
            label = self.bubble_chamber.create_label(
                target_concept,
                self.target_group.location,
                confidence_of_class_affinity,
            )
            self.target_group.add_label(label)
            return self._engender_follow_up(confidence_of_class_affinity)
        return self._engender_alternative_follow_up(confidence_of_class_affinity)

    def _get_target_concept(self) -> Concept:
        group_member = self.target_group.get_random_member()
        labels = [
            label
            for label in group_member.labels
            if label.strengh > self.CONFIDENCE_THRESHOLD
        ]
        target_label = random.choice(labels)
        return target_label.parent_concept

    def _calculate_confidence(self, target_concept: Concept) -> float:
        total_strength = 0.0
        for member in self.target_group.members:
            for label in member.labels:
                if label.parent_concept == target_concept:
                    total_strength += label.strength
        average_strength = total_strength / self.target_group.size
        return average_strength

    def _engender_follow_up(self, urgency: float) -> Codelet:
        return GroupExtender(self.bubble_chamber, self.target_group, urgency)

    def _engender_alternative_follow_up(self, urgency: float) -> Codelet:
        return GroupLabeler(self.bubble_chamber, self.target_group, urgency)
