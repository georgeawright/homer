from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.hyper_parameters import HyperParameters
from homer.perceptlets.correspondence import Correspondence
from homer.perceptlet_collection import PerceptletCollection


class CorrespondenceLabeler(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        relevant_space: Concept,
        target_correspondence: Correspondence,
        urgency: float,
        parent_id: str,
    ):
        parent_concept = None
        Codelet.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            parent_concept,
            target_correspondence,
            urgency,
            parent_id,
        )
        self.relevant_space = relevant_space

    def _passes_preliminary_checks(self) -> bool:
        self.parent_concept = self.bubble_chamber.get_random_correspondence_type()
        return True

    def _fizzle(self) -> CorrespondenceLabeler:
        self.perceptlet_type.decay_activation(self.target_perceptlet.location)
        return self._engender_alternative_follow_up()

    def _calculate_confidence(self):
        number_of_shared_labels = len(
            PerceptletCollection.intersection(
                self.target_perceptlet.first_argument.labels,
                self.target_perceptlet.second_argument.labels,
            )
        )
        proximity = self.relevant_space.proximity_between(
            self.target_perceptlet.first_argument.get_value(self.relevant_space),
            self.target_perceptlet.second_argument.get_value(self.relevant_space),
        )
        self.confidence = self.parent_concept.calculate_affinity(
            number_of_shared_labels, proximity
        )

    def _process_perceptlet(self):
        label = self.bubble_chamber.create_label(
            self.parent_concept,
            self.target_perceptlet.location,
            self.confidence,
            self.codelet_id,
        )
        self.target_perceptlet.labels.add(label)

    def _engender_follow_up(self) -> Codelet:
        from homer.codelets.correspondence_builder import CorrespondenceBuilder

        return CorrespondenceBuilder(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "correspondence"
            ),
            self.relevant_space,
            self.target_perceptlet.first_argument,
            self.target_perceptlet.second_argument,
            self.confidence,
            self.codelet_id,
        )

    def _engender_alternative_follow_up(self):
        return CorrespondenceLabeler(
            self.bubble_chamber,
            self.perceptlet_type,
            self.relevant_space,
            self.target_perceptlet,
            self.urgency / 2,
            self.parent_id,
        )
