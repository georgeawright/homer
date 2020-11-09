from abc import abstractmethod

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure


class Evaluator(Codelet):
    """Evaluates the quality of target_structure and adjusts its quality accordingly."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        target_structure: Structure,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.target_structure = target_structure

    def run(self):
        self._calculate_confidence()
        self.target_structure.quality += self.confidence
        self._engender_follow_up()
        self.result = CodeletResult.SUCCESS
        return self.result

    @abstractmethod
    def _calculate_confidence(self):
        pass
