from __future__ import annotations
from abc import abstractclassmethod
import statistics

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID


class ViewSuggester(Suggester):
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
        self.frame = target_structures.get("frame")
        self.contextual_space = target_structures.get("contextual_space")
        self.conceptual_spaces_map = {}

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

    @abstractclassmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber, urgency: float = None):
        pass

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    @property
    def targets_dict(self):
        return {
            "frame": self.frame,
            "contextual_space": self.contextual_space,
            "conceptual_spaces_map": self.conceptual_spaces_map,
        }

    def _passes_preliminary_checks(self):
        return True

    def _calculate_confidence(self):
        self.confidence = statistics.fmean(
            [
                (1 - self.bubble_chamber.focus.focussedness),
                self.frame.activation,
                self.contextual_space.activation,
            ]
        )

    def _fizzle(self):
        pass
