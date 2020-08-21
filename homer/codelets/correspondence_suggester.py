from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.bubbles.perceptlets import Group
from homer.codelet import Codelet

from .group_labeler import GroupLabeler


class CorrespondenceSuggester(Codelet):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_group_a: Group,
        target_group_b: Group,
        urgency: float,
        parent_id: str,
    ):
        parent_concept = None
        Codelet.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            parent_concept,
            target_group_a,
            urgency,
            parent_id,
        )
        self.second_target_perceptlet = target_group_b

    def _passes_preliminary_checks(self) -> bool:
        if (
            len(self.target_perceptlet.labels) == 0
            or len(self.second_target_perceptlet.labels) == 0
        ):
            return False
        self.parent_concept = (
            self.target_perceptlet.labels.get_random().parent_concept.space
        )
        return True

    def _fizzle(self) -> GroupLabeler:
        self.perceptlet_type.decay_activation(self.target_perceptlet.location)
        if len(self.target_perceptlet.labels) == 0:
            return self._engender_group_labeler(self.target_perceptlet)
        return self._engender_group_labeler(self.second_target_perceptlet)

    def _fail(self) -> CorrespondenceSuggester:
        self.perceptlet_type.decay_activation(self.target_perceptlet.location)
        return CorrespondenceSuggester(
            self.bubble_chamber,
            self.perceptlet_type,
            *self.bubble_chamber.get_random_groups(2),
            self.urgency / 2,
            self.codelet_id,
        )

    def _calculate_confidence(self):
        self.confidence = float(
            self.second_target_perceptlet.has_label_in_space(self.parent_concept)
            and not self.target_perceptlet.has_correspondence(
                self.second_target_perceptlet, self.parent_concept
            )
        )

    def _process_perceptlet(self):
        pass

    def _engender_follow_up(self):
        from homer.codelets.correspondence_builder import CorrespondenceBuilder

        return CorrespondenceBuilder(
            self.bubble_chamber,
            self.perceptlet_type,
            self.parent_concept,
            self.target_perceptlet,
            self.second_target_perceptlet,
            self.urgency,
            self.codelet_id,
        )

    def _engender_group_labeler(self, target_group: Group):
        return GroupLabeler(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "group-label"
            ),
            target_group,
            self.urgency,
            self.codelet_id,
        )
