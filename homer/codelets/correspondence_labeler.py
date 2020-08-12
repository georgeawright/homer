from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concepts.perceptlet_type import PerceptletType
from homer.hyper_parameters import HyperParameters
from homer.perceptlets.correspondence import Correspondence


class CorrespondenceLabeler(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_correspondence: Correspondence,
        urgency: float,
        parent_id: str,
    ):
        Codelet.__init__(self, bubble_chamber, parent_id)
        self.bubble_chamber = bubble_chamber
        self.perceptlet_type = perceptlet_type
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
                self.perceptlet_type.boost_activation(confidence_of_affinity, [])
                label = self.bubble_chamber.create_label(
                    concept,
                    self.target_correspondence.location,
                    confidence_of_affinity,
                    self.codelet_id,
                )
                self.target_correspondence.add_label(label)
                print(
                    f"CORRESPONDENCE LABELED: {self.target_correspondence.target_group_a.location} to {self.target_correspondence.target_group_b.location} with {concept.name}"
                )
                confidence = max(confidence, confidence_of_affinity)
            else:
                self.perceptlet_type.decay_activation(
                    self.target_correspondence.location
                )
        if confidence > self.CONFIDENCE_THRESHOLD:
            return self._engender_follow_up(confidence)

    def _engender_follow_up(self, urgency: float) -> Codelet:
        from homer.codelets.correspondence_builder import CorrespondenceBuilder

        return CorrespondenceBuilder(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "correspondence"
            ),
            None,
            self.target_correspondence.target_group_a,
            self.target_correspondence.target_group_b,
            urgency,
            self.codelet_id,
        )
