from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.classifiers import LabelClassifier
from homer.codelets.evaluator import Evaluator


class LabelEvaluator(Evaluator):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        target_label: Perceptlet,
        urgency: float,
        parent_id: str,
    ):
        Evaluator.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            target_type,
            target_label,
            urgency,
            parent_id,
        )
        self.target_label = target_label
        self.parent_concept = target_label.parent_concept
        self.classifier = LabelClassifier()

    def _passes_preliminary_checks(self) -> bool:
        return True

    def _calculate_confidence(self):
        quality_estimate = self.classifier.confidence(
            self.target_label.target, self.parent_concept
        )
        self.confidence = quality_estimate - self.target_label.quality
