from __future__ import annotations

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.bubbles.perceptlets import Group
from homer.codelet import Codelet


class GroupExtender(Codelet):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_group: Group,
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

    def _passes_preliminary_checks(self) -> bool:
        if len(self.target_perceptlet.neighbours) == 0:
            return False
        self.second_target_perceptlet = self.target_perceptlet.neighbours.get_random()
        if self.second_target_perceptlet.makes_group_with(
            self.target_perceptlet.members
        ):
            return False
        return True

    def _fizzle(self) -> GroupExtender:
        self._decay_concept(self.perceptlet_type)
        return self._engender_alternative_follow_up()

    def _fail(self):
        self._decay_concept(self.perceptlet_type)
        return None

    def _calculate_confidence(self):
        spaces = {label.parent_concept.space for label in self.target_perceptlet.labels}
        distances = [
            space.proximity_between(
                self.target_perceptlet.get_value(space),
                self.second_target_perceptlet.get_value(space),
            )
            for space in spaces
        ]
        self.confidence = 0.0 if distances == [] else fuzzy.OR(*distances)

    def _process_perceptlet(self):
        self.target_perceptlet.add_member(self.second_target_perceptlet)
        self.second_target_perceptlet.add_group(self.target_perceptlet)

    def _engender_follow_up(self) -> GroupExtender:
        return GroupExtender(
            self.bubble_chamber,
            self.perceptlet_type,
            self.target_perceptlet,
            self.confidence,
            self.codelet_id,
        )

    def _engender_alternative_follow_up(self) -> GroupExtender:
        return GroupExtender(
            self.bubble_chamber,
            self.perceptlet_type,
            self.target_perceptlet,
            self.urgency / 2,
            self.codelet_id,
        )
