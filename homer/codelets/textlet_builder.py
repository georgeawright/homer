from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concepts.perceptlet_type import PerceptletType
from homer.perceptlets import Group


class TextletBuilder(Codelet):
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

    def _passes_preliminary_checks(self) -> bool:
        if len(self.target_perceptlet.labels) == 0:
            return False
        self.target_label = self.target_perceptlet.labels.get_random()
        self.parent_concept = self.target_label.parent_concept.space
        self.template = self.parent_concept.get_template()
        return not self.target_perceptlet.has_textlet(self.template, self.target_label)

    def _fizzle(self):
        self.perceptlet_type.decay_activation(self.target_perceptlet.location)
        return self._engender_alternative_follow_up()

    def _calculate_confidence(self):
        self.confidence = self.target_label.strength

    def _process_perceptlet(self):
        textlet = self.bubble_chamber.create_textlet(
            self.template, self.target_label, self.confidence, self.codelet_id,
        )
        self.target_perceptlet.textlets.add(textlet)

    def _engender_follow_up(self) -> TextletBuilder:
        return TextletBuilder(
            self.bubble_chamber,
            self.perceptlet_type,
            self.bubble_chamber.workspace.groups.get_exigent(),
            self.confidence,
            self.codelet_id,
        )

    def _engender_alternative_follow_up(self) -> TextletBuilder:
        return TextletBuilder(
            self.bubble_chamber,
            self.perceptlet_type,
            self.bubble_chamber.workspace.groups.get_exigent(),
            self.urgency / 2,
            self.codelet_id,
        )
