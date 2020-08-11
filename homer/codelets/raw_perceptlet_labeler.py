from typing import Optional

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet


class RawPerceptletLabeler(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        parent_concept: Concept,
        target_perceptlet: Optional[Perceptlet],
        urgency: float,
        parent_id: str,
    ):
        Codelet.__init__(self, bubble_chamber, parent_id)
        self.parent_concept = parent_concept
        self.perceptlet_type = perceptlet_type
        self.target_perceptlet = target_perceptlet
        self.urgency = urgency

    def run(self) -> Optional[Codelet]:
        if not self.target_perceptlet.has_label(self.parent_concept):
            confidence_of_class_membership = self._calculate_confidence(
                self.parent_concept.get_activation(self.target_perceptlet.location),
                self.parent_concept.depth_rating,
                self.parent_concept.proximity_to(
                    self.target_perceptlet.get_value(self.parent_concept)
                ),
                self.target_perceptlet.proportion_of_neighbours_with_label(
                    self.parent_concept
                ),
            )
            if confidence_of_class_membership > self.CONFIDENCE_THRESHOLD:
                self.parent_concept.boost_activation(
                    confidence_of_class_membership, self.target_perceptlet.location
                )
                self.perceptlet_type.boost_activation(
                    confidence_of_class_membership, self.target_perceptlet.location
                )
                label = self.bubble_chamber.create_label(
                    self.parent_concept,
                    self.target_perceptlet.location,
                    confidence_of_class_membership,
                    self.codelet_id,
                )
                self.target_perceptlet.add_label(label)
                print(
                    f"LABEL (top_down): {self.target_perceptlet.value} at {self.target_perceptlet.location} with {self.parent_concept.name}, confidence: {label.strength}"
                )
                return self.engender_follow_up(confidence_of_class_membership)
        self.perceptlet_type.decay_activation([])
        return None

    def _calculate_confidence(
        self,
        concept_activation: float,
        concept_depth_rating: float,
        proximity_to_prototype: float,
        proportion_of_neighbours: float,
    ) -> float:
        return fuzzy.OR(
            # concept_depth_rating,
            proximity_to_prototype,
            # concept_activation,
            proportion_of_neighbours,
        )

    def engender_follow_up(self, confidence: float) -> Codelet:
        new_target = self.target_perceptlet.most_exigent_neighbour()
        return RawPerceptletLabeler(
            self.bubble_chamber,
            self.perceptlet_type,
            self.parent_concept,
            new_target,
            confidence,
            self.codelet_id,
        )
