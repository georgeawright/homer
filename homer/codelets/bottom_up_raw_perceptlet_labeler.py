from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelets.raw_perceptlet_labeler import RawPerceptletLabeler
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet


class BottomUpRawPerceptletLabeler(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_perceptlet: Perceptlet,
        urgency: float,
        parent_id: str,
    ):
        Codelet.__init__(self, bubble_chamber, parent_id)
        self.perceptlet_type = perceptlet_type
        self.target_perceptlet = target_perceptlet
        self.urgency = urgency

    def run(self):
        concept = self.bubble_chamber.get_random_workspace_concept()
        if self.target_perceptlet.has_label(concept):
            self.perceptlet_type.decay_activation(self.target_perceptlet.location)
            return None
        else:
            confidence_of_class_membership = concept.proximity_to(
                self.target_perceptlet.get_value(concept)
            )
            if confidence_of_class_membership > self.CONFIDENCE_THRESHOLD:
                concept.boost_activation(
                    confidence_of_class_membership, self.target_perceptlet.location
                )
                self.perceptlet_type.boost_activation(
                    confidence_of_class_membership, self.target_perceptlet.location
                )
                label = self.bubble_chamber.create_label(
                    concept,
                    self.target_perceptlet.location,
                    confidence_of_class_membership,
                    self.codelet_id,
                )
                self.target_perceptlet.add_label(label)
                print(
                    f"LABEL (bottom_up): {self.target_perceptlet.value} at {self.target_perceptlet.location} with {concept.name}, confidence: {label.strength}"
                )
                return self._engender_follow_up(concept, confidence_of_class_membership)
        return self._engender_alternative_follow_up(confidence_of_class_membership)

    def _engender_follow_up(self, concept: Concept, urgency: float) -> Codelet:
        new_target_perceptlet = self.target_perceptlet.get_random_neighbour()
        return RawPerceptletLabeler(
            self.bubble_chamber,
            self.perceptlet_type,
            concept,
            new_target_perceptlet,
            urgency,
            self.codelet_id,
        )

    def _engender_alternative_follow_up(self, urgency: float) -> Codelet:
        new_target_perceptlet = self.bubble_chamber.get_raw_perceptlet()
        return BottomUpRawPerceptletLabeler(
            self.bubble_chamber,
            self.perceptlet_type,
            new_target_perceptlet,
            urgency,
            self.codelet_id,
        )
