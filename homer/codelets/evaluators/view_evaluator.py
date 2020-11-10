import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator
from homer.codelets.selectors import ViewSelector
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure


class ViewEvaluator(Evaluator):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structure: Structure,
        urgency: FloatBetweenOneAndZero,
    ):
        Evaluator.__init__(self, codelet_id, parent_id, target_structure, urgency)
        self.bubble_chamber = bubble_chamber

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structure: Structure,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, target_structure, urgency)

    def _calculate_confidence(self):
        quality_estimate = statistics.fmean(
            [member.quality for member in self.target_structure.members]
        )
        self.confidence = quality_estimate - self.target_structure.quality

    def _engender_follow_up(self):
        self.child_codelets.append(
            ViewSelector.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_structure,
                self.confidence,
            )
        )
