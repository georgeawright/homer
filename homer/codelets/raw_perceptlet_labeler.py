from typing import Optional

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concept import Concept
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet


class RawPerceptletLabeler(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        target_perceptlet: Optional[Perceptlet],
        urgency: float,
    ):
        Codelet.__init__(self, bubble_chamber)
        self.parent_concept = parent_concept
        self.target_perceptlet = target_perceptlet
        self.urgency = urgency

    def run(self) -> Optional[Codelet]:
        confidence_of_class_membership = self._calculate_confidence(
            self.parent_concept.get_activation(self.target_perceptlet.location),
            self.parent_concept.depth_rating,
            self.parent_concept.distance_rating(
                self.target_perceptlet.get_value(self.parent_concept)
            ),
            self.target_perceptlet.proportion_of_neighbours_with_label(
                self.parent_concept
            ),
        )
        if confidence_of_class_membership > self.CONFIDENCE_THRESHOLD:
            self.parent_concept.boost_activation(confidence_of_class_membership)
            label = self.bubble_chamber.create_label(
                self.parent_concept,
                self.target_perceptlet.location,
                confidence_of_class_membership,
            )
            self.target_perceptlet.add_label(label)
            return self.engender_follow_up(confidence_of_class_membership)
        return None

    def _calculate_confidence(
        self,
        concept_activation: float,
        concept_depth: float,
        distance_from_prototype: float,
        proportion_of_neighbours: float,
    ) -> float:
        return fuzzy.AND(
            fuzzy.NAND(concept_depth, distance_from_prototype),
            fuzzy.OR(concept_activation, proportion_of_neighbours),
        )

    def engender_follow_up(self, confidence: float) -> Codelet:
        new_target = self.target_perceptlet.most_exigent_neighbour()
        return RawPerceptletLabeler(
            self.bubble_chamber, self.parent_concept, new_target, confidence,
        )
