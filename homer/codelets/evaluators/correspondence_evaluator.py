from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.classifiers import CorrespondenceClassifier
from homer.codelets.evaluator import Evaluator
from homer.codelets.selectors.correspondence_selector import CorrespondenceSelector


class CorrespondenceEvaluator(Evaluator):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        target_correspondence: Perceptlet,
        urgency: float,
        parent_id: str,
    ):
        Evaluator.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            target_type,
            target_correspondence,
            urgency,
            parent_id,
        )
        self.target_correspondence = target_correspondence
        self.classifier = CorrespondenceClassifier()

    def _passes_preliminary_checks(self) -> bool:
        return True

    def _calculate_confidence(self):
        quality_estimate = self.classifier.confidence(
            self.target_correspondence.first_argument,
            self.target_correspondence.second_argument,
            self.target_correspondence.parent_concept,
        )
        self.confidence = quality_estimate - self.target_correspondence.quality

    def _engender_follow_up(self) -> CorrespondenceSelector:
        return CorrespondenceSelector(
            self.bubble_chamber,
            self.bubble_chamber.concept_space["correspondence-selection"],
            self.target_type,
            self.bubble_chamber.workspace.correspondences.at(
                self.location
            ).get_most_active(),
            self.urgency,
            self.codelet_id,
        )
