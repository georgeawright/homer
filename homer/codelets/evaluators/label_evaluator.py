from homer.codelets.evaluator import Evaluator
from homer.codelets.selectors import LabelSelector
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure


class LabelEvaluator(Evaluator):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        target_structure: Structure,
        urgency: FloatBetweenOneAndZero,
    ):
        Evaluator.__init__(self, codelet_id, parent_id, target_structure, urgency)

    def _calculate_confidence(self):
        quality_estimate = self.target_structure.parent_concept.classify(
            self.target_structure.start
        )
        self.confidence = quality_estimate - self.target_structure.quality

    def _engender_follow_up(self):
        self.child_codelets.append(
            LabelSelector.spawn(self.codelet_id, self.confidence)
        )