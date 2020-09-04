from __future__ import annotations
import random
from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Concept
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.bubbles.perceptlets import Group
from homer.classifiers import GroupLabelClassifier
from homer.codelet import Codelet

from .group_extender import GroupExtender


class GroupLabeler(Codelet):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_group: Optional[Group],
        urgency: float,
        parent_id: str,
    ):
        parent_concept = None
        Codelet.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            parent_concept,
            target_group,
            urgency,
            parent_id,
        )
        self.classifier = GroupLabelClassifier()

    def _passes_preliminary_checks(self) -> bool:
        try:
            self.parent_concept = self._get_target_concept()
        except IndexError:
            return False
        return not self.target_perceptlet.has_label(self.parent_concept)

    def _fizzle(self) -> GroupLabeler:
        self._decay_concept(self.perceptlet_type)
        return self._engender_alternative_follow_up()

    def _fail(self) -> GroupLabeler:
        self._decay_concept(self.perceptlet_type)
        self._decay_concept(self.parent_concept)
        return self._engender_alternative_follow_up()

    def _calculate_confidence(self):
        self.confidence = self.classifier.confidence(
            self.target_perceptlet, self.parent_concept
        )

    def _process_perceptlet(self):
        label = self.bubble_chamber.create_label(
            self.parent_concept,
            self.target_perceptlet.location,
            self.target_perceptlet,
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
            self.perceptlet_type.activation.at(self.location),
            self.codelet_id,
        )

    def _get_target_concept(self) -> Concept:
        group_member = self.target_perceptlet.members.get_random()
        labels = [
            label
            for label in group_member.labels
            if label.activation.as_scalar() > self.CONFIDENCE_THRESHOLD
        ]
        target_label = random.choice(labels)
        return target_label.parent_concept
