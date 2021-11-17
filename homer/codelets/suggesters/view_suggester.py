from __future__ import annotations
from abc import abstractclassmethod
import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID


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
        self._target_structures = target_structures
        self.input_spaces = None
        self.output_space = None
        self.frame = None
        self.contextual_space = None

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

    def _passes_preliminary_checks(self):
        self.frame = self._target_structures["frame"]
        self.contextual_space = self._target_structures["contextual_space"]
        return True

    def _calculate_confidence(self):
        self.confidence = statistics.fmean(
            [self.frame.activation, self.contextual_space.activation]
        )

    def _fizzle(self):
        pass
