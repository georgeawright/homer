from __future__ import annotations
from typing import Optional

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Concept, Perceptlet
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.classifiers import LabelClassifier
from homer.codelet import Codelet


class RawPerceptletLabeler(Codelet):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        parent_concept: Concept,
        target_perceptlet: Optional[Perceptlet],
        urgency: float,
        parent_id: str,
    ):
        Codelet.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            parent_concept,
            target_perceptlet,
            urgency,
            parent_id,
        )
        self.classifier = LabelClassifier()

    def _passes_preliminary_checks(self) -> bool:
        return not self.target_perceptlet.has_label(self.parent_concept)

    def _fizzle(self):
        return self._engender_alternative_follow_up()

    def _fail(self):
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
        self.bubble_chamber.logger.log_perceptlet_connection(
            self, self.target_perceptlet, label
        )

    def _engender_follow_up(self) -> RawPerceptletLabeler:
        new_target = self.target_perceptlet.neighbours.get_unhappy()
        return RawPerceptletLabeler(
            self.bubble_chamber,
            self.perceptlet_type,
            self.parent_concept,
            new_target,
            self.confidence,
            self.codelet_id,
        )

    def _engender_alternative_follow_up(self) -> Codelet:
        from .bottom_up_raw_perceptlet_labeler import BottomUpRawPerceptletLabeler

        return BottomUpRawPerceptletLabeler(
            self.bubble_chamber,
            self.perceptlet_type,
            self.target_perceptlet,
            self.target_perceptlet.unhappiness.as_scalar(),
            self.codelet_id,
        )
