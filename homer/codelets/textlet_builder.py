from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.bubbles.perceptlets import Group
from homer.codelet import Codelet

from .group_labeler import GroupLabeler


class TextletBuilder(Codelet):
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
        if len(self.target_perceptlet.labels) == 0:
            return False
        self.target_label = self.target_perceptlet.labels.get_random()
        self.parent_concept = self.target_label.parent_concept.space
        self.template = self.parent_concept.get_template()
        return not self.target_perceptlet.has_textlet(self.template, self.target_label)

    def _fizzle(self) -> GroupLabeler:
        self._decay_concept(self.perceptlet_type)
        return GroupLabeler(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "group-label"
            ),
            self.target_perceptlet,
            self.urgency,
            self.codelet_id,
        )

    def _fail(self) -> TextletBuilder:
        self._decay_concept(self.perceptlet_type)
        self._decay_concept(self.parent_concept)
        self.urgency /= 2
        return self._engender_follow_up()

    def _calculate_confidence(self):
        self.confidence = self.target_label.activation.as_scalar()

    def _process_perceptlet(self):
        textlet = self.bubble_chamber.create_textlet(
            self.template,
            self.target_label,
            self.confidence,
            self.codelet_id,
        )
        self.target_perceptlet.add_textlet(textlet)
        self.bubble_chamber.logger.log_perceptlet_connection(
            self, self.target_perceptlet, textlet
        )
        self.child_perceptlet = textlet

    def _engender_follow_up(self) -> TextletBuilder:
        return TextletBuilder(
            self.bubble_chamber,
            self.perceptlet_type,
            self.bubble_chamber.workspace.groups.get_exigent(),
            self.confidence,
            self.codelet_id,
        )
