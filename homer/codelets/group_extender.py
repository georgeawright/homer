from __future__ import annotations

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concepts.perceptlet_type import PerceptletType

from homer.perceptlets.group import Group


class GroupExtender(Codelet):
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
        self.target_perceptlet = target_group
        self.urgency = urgency
        self.parent_concept = None

    def _passes_preliminary_checks(self) -> bool:
        if len(self.target_perceptlet.neighbours) == 0:
            return False
        self.second_target_perceptlet = self.target_perceptlet.neighbours.get_random()
        return True

    def _fizzle(self):
        self.perceptlet_type.decay_activation(self.target_perceptlet.location)
        return None

    def _calculate_confidence(self):
        common_concepts = set.intersection(
            {label.parent_concept for label in self.target_perceptlet.labels},
            {label.parent_concept for label in self.second_target_perceptlet.labels},
        )
        distances = [
            concept.proximity_between(
                self.target_perceptlet.get_value(concept),
                self.second_target_perceptlet.get_value(concept),
            )
            for concept in common_concepts
        ]
        self.confidence = 0.0 if distances == [] else fuzzy.OR(*distances)

    def _process_perceptlet(self):
        self.target_perceptlet.members.add(self.second_target_perceptlet)
        self.second_target_perceptlet.groups.add(self.target_perceptlet)

    def _engender_follow_up(self) -> GroupExtender:
        return GroupExtender(
            self.bubble_chamber,
            self.perceptlet_type,
            self.target_perceptlet,
            self.confidence,
            self.codelet_id,
        )
