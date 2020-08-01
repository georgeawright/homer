from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelets.raw_perceptlet_labeler import RawPerceptletLabeler
from homer.concept import Concept
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet


class BottomUpRawPerceptletLabeler(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        target_perceptlet: Perceptlet,
        urgency: float,
    ):
        self.bubble_chamber = bubble_chamber
        self.target_perceptlet = target_perceptlet
        self.urgency = urgency

    def run(self):
        concept = self.bubble_chamber.get_random_workspace_concept()
        confidence_of_class_membership = concept.proximity_to(
            self.target_perceptlet.get_value(concept)
        )
        if confidence_of_class_membership > self.CONFIDENCE_THRESHOLD:
            concept.boost_activation(
                confidence_of_class_membership, self.target_perceptlet.location
            )
            label = self.bubble_chamber.create_label(
                concept, self.target_perceptlet.location, confidence_of_class_membership
            )
            self.target_perceptlet.add_label(label)
            return self._engender_follow_up(concept, confidence_of_class_membership)
        return self._engender_alternative_follow_up(confidence_of_class_membership)

    def _engender_follow_up(self, concept: Concept, urgency: float) -> Codelet:
        new_target_perceptlet = self.target_perceptlet.get_random_neighbour
        return RawPerceptletLabeler(
            self.bubble_chamber, concept, new_target_perceptlet, urgency
        )

    def _engender_alternative_follow_up(self, urgency: float) -> Codelet:
        new_target_perceptlet = self.bubble_chamber.get_raw_perceptlet()
        return BottomUpRawPerceptletLabeler(
            self.bubble_chamber, new_target_perceptlet, urgency
        )
