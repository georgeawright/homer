from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator
from homer.codelets.selectors import LabelSelector
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structures.links import Label


class LabelEvaluator(Evaluator):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structure: Label,
        urgency: FloatBetweenOneAndZero,
    ):
        Evaluator.__init__(self, codelet_id, parent_id, target_structure, urgency)
        self.bubble_chamber = bubble_chamber
        self.original_confidence = self.target_structure.quality

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structure: Label,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, target_structure, urgency)

    def _calculate_confidence(self):
        self.confidence = self.target_structure.parent_concept.classifier.classify(
            {
                "start": self.target_structure.start,
                "concept": self.target_structure.parent_concept,
            }
        )

    def _engender_follow_up(self):
        self.child_codelets.append(
            LabelSelector.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_structure,
                abs(self.confidence - self.original_confidence),
            )
        )
