from __future__ import annotations
import statistics

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelet import Codelet

from .raw_perceptlet_labeler import RawPerceptletLabeler


class BottomUpRawPerceptletLabeler(Codelet):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_perceptlet: Perceptlet,
        urgency: float,
        parent_id: str,
    ):
        parent_concept = None
        Codelet.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            parent_concept,
            target_perceptlet,
            urgency,
            parent_id,
        )

    def _passes_preliminary_checks(self) -> bool:
        self.parent_concept = self.bubble_chamber.get_random_workspace_concept()
        return not self.target_perceptlet.has_label(self.parent_concept)

    def _fizzle(self):
        return self._fail()

    def _fail(self):
        self.perceptlet_type.decay_activation(self.target_perceptlet.location)
        return self._engender_alternative_follow_up()

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.proximity_to(
            self.target_perceptlet.get_value(self.parent_concept)
        )

    def _process_perceptlet(self):
        label = self.bubble_chamber.create_label(
            self.parent_concept,
            self.target_perceptlet.location,
            self.confidence,
            self.codelet_id,
        )
        self.target_perceptlet.labels.add(label)

    def _engender_follow_up(self) -> RawPerceptletLabeler:
        new_target_perceptlet = self.target_perceptlet.neighbours.get_unhappy()
        return RawPerceptletLabeler(
            self.bubble_chamber,
            self.perceptlet_type,
            self.parent_concept,
            new_target_perceptlet,
            self.confidence,
            self.codelet_id,
        )

    def _engender_alternative_follow_up(self) -> BottomUpRawPerceptletLabeler:
        new_target_perceptlet = (
            self.bubble_chamber.workspace.raw_perceptlets.get_unhappy()
        )
        perceptlet_type_activation = self.perceptlet_type.activation.at(
            new_target_perceptlet.location
        )
        new_urgency = statistics.fmean([self.urgency, perceptlet_type_activation])
        return BottomUpRawPerceptletLabeler(
            self.bubble_chamber,
            self.perceptlet_type,
            new_target_perceptlet,
            new_urgency,
            self.codelet_id,
        )
