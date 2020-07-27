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
        parent_concept: Concept,
        target_group: Optional[Group],
        urgency: float,
    ):
        Codelet.__init__(self, bubble_chamber)
        self.parent_concept = parent_concept
        self.target_group = target_group
        self.urgency = urgency

    def run(self) -> Optional[Codelet]:
        confidence_of_class_membership = self.calculate_confidence()
        if confidence_of_class_membership > self.CONFIDENCE_THRESHOLD:
            self.parent_concept.boost_activation(confidence_of_class_membership)
            label = self.bubble_chamber.create_label(
                self.parent_concept,
                self.target_group.location,
                self.target_group.time,
                confidence_of_class_membership,
            )
            self.target_perceptlet.add_label(label)
            return self.engender_follow_up(confidence_of_class_membership)
        return None

    def _calculate_confidence(self) -> float:
        return (
            sum(
                label.strength
                for member in self.target_group.members
                for label in member.labels
                if label.parent_concept == self.parent_concept
            )
            / self.target_group.size
        )

    def engender_follow_up(self, urgency: float) -> Codelet:
        return GroupExtender(self.bubble_chamber, self.target_group, urgency)
