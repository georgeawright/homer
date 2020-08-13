from __future__ import annotations
import random
from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelets.group_extender import GroupExtender
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.perceptlets.group import Group


class GroupLabeler(Codelet):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_group: Optional[Group],
        urgency: float,
        parent_id: str,
    ):
        Codelet.__init__(self, bubble_chamber, parent_id)
        self.perceptlet_type = perceptlet_type
        self.target_perceptlet = target_group
        self.urgency = urgency

    def _passes_preliminary_checks(self) -> bool:
        self.parent_concept = self._get_target_concept()
        return not self.target_perceptlet.has_label(self.parent_concept)

    def _fizzle(self) -> GroupLabeler:
        self.perceptlet_type.decay_activation(self.target_perceptlet.location)
        return self._engender_alternative_follow_up()

    def _calculate_confidence(self):
        total_strength = 0.0
        for member in self.target_perceptlet.members:
            for label in member.labels:
                if label.parent_concept == self.parent_concept:
                    total_strength += label.strength
        self.confidence = total_strength / self.target_perceptlet.size

    def _process_perceptlet(self):
        label = self.bubble_chamber.create_label(
            self.parent_concept,
            self.target_perceptlet.location,
            self.confidence,
            self.codelet_id,
        )
        self.target_perceptlet.add_label(label)

    def _engender_follow_up(self) -> GroupExtender:
        return GroupExtender(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name("group"),
            self.target_perceptlet,
            self.confidence,
            self.codelet_id,
        )

    def _engender_alternative_follow_up(self) -> GroupLabeler:
        return GroupLabeler(
            self.bubble_chamber,
            self.perceptlet_type,
            self.target_perceptlet,
            self.urgency / 2,
            self.codelet_id,
        )

    def _get_target_concept(self) -> Concept:
        group_member = self.target_perceptlet.get_random_member()
        labels = [
            label
            for label in group_member.labels
            if label.strength > self.CONFIDENCE_THRESHOLD
        ]
        target_label = random.choice(labels)
        return target_label.parent_concept
