from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.hyper_parameters import HyperParameters
from homer.perceptlets.correspondence import Correspondence


class CorrespondenceLabeler(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        target_correspondence: Correspondence,
        urgency: float,
    ):
        self.bubble_chamber = bubble_chamber
        self.target_correspondence = target_correspondence
        self.urgency = urgency

    def run(self):
        confidence = 0.0
        for concept in self.bubble_chamber.concept_space.correspondence_concepts:
            confidence_of_affinity = concept.confidence_of_affinity(
                self.target_correspondence.target_group_a,
                self.target_correspondence.target_group_b,
            )
            if confidence_of_affinity > self.CONFIDENCE_THRESHOLD:
                self.bubble_chamber.add_label(
                    concept, self.target_correspondence, confidence_of_affinity
                )
                confidence = max(confidence, confidence_of_affinity)
        if confidence > self.CONFIDENCE_THRESHOLD:
            self._engender_follow_up(confidence)

    def _engender_follow_up(self, urgency: float) -> Codelet:
        from homer.codelets.correspondence_builder import CorrespondenceBuilder

        return CorrespondenceBuilder(
            self.bubble_chamber,
            None,
            self.target_correspondence.target_group_a,
            self.target_correspondence.target_group_b,
            urgency,
        )
