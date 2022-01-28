from __future__ import annotations

import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID


class ProjectionSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.target_view = target_structures.get("target_view")
        self.target_projectee = target_structures.get("target_projectee")
        self.frame = target_structures.get("frame")

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @property
    def targets_dict(self):
        return {
            "target_view": self.target_view,
            "target_projectee": self.target_projectee,
            "frame": self.frame,
        }

    def _passes_preliminary_checks(self):
        raise NotImplementedError

    def _calculate_confidence(self):
        self.confidence = statistics.fmean(
            [space.quality for space in self.target_view.input_spaces]
        )

    def _fizzle(self):
        pass
