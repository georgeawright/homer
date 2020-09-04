from __future__ import annotations
from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelets.evaluators.label_evaluator import LabelEvaluator
from homer.errors import MissingPerceptletError


class RawPerceptletLabelEvaluator(LabelEvaluator):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        target_label: Perceptlet,
        urgency: float,
        parent_id: str,
    ):
        LabelEvaluator.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            target_type,
            target_label,
            urgency,
            parent_id,
        )

    def _engender_follow_up(self) -> Optional[RawPerceptletLabelEvaluator]:
        try:
            raw_perceptlet = self.bubble_chamber.workspace.raw_perceptlets.get_active()
            label = raw_perceptlet.labels.get_active()
        except MissingPerceptletError:
            return None
        return RawPerceptletLabelEvaluator(
            self.bubble_chamber,
            self.perceptlet_type,
            self.target_type,
            label,
            self.urgency,
            self.codelet_id,
        )
