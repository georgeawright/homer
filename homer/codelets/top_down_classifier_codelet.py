from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concept import Concept
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet


class TopDownClassifierCodelet(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        target_perceptlet: Optional[Perceptlet],
        classification_weights,
        urgency: float,
    ):
        Codelet.__init__(self, bubble_chamber)
        self.parent_concept = parent_concept
        self.target_perceptlet = target_perceptlet
        self.classification_weights = classification_weights
        self.urgency = urgency

    def run(self) -> Optional[Codelet]:
        confidence_of_class_membership = self.calculate_confidence(
            [
                self.parent_concept.activation,
                self.parent_concept.depth,
                self.parent_concept.distance_from(self.target_perceptlet.value),
                self.target_perceptlet.proportion_of_neighbours_with_label(
                    self.parent_concept
                ),
            ]
        )
        self.parent_concept.boost_activation(confidence_of_class_membership)
        if confidence_of_class_membership > self.CONFIDENCE_THRESHOLD:
            label = self.bubble_chamber.create_label(
                self.parent_concept, confidence_of_class_membership
            )
            self.target_perceptlet.add_label(label)
            return self.engender_follow_up(confidence_of_class_membership)
        return None

    def calculate_confidence(self, inputs) -> float:
        return sum(i[0] * i[1] for i in zip(inputs, self.classification_weights))

    def engender_follow_up(self, confidence: float) -> Codelet:
        return TopDownClassifierCodelet(
            self.bubble_chamber,
            self.parent_concept,
            None,
            self.classification_weights,
            confidence,
        )
