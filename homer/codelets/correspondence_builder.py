from typing import Optional

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.hyper_parameters import HyperParameters
from homer.perceptlets.correspondence import Correspondence
from homer.perceptlets.group import Group


class CorrespondenceBuilder(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        parent_space: Concept,
        target_group_a: Group,
        target_group_b: Group,
        urgency: float,
    ):
        self.bubble_chamber = bubble_chamber
        self.perceptlet_type = perceptlet_type
        self.parent_space = parent_space
        self.target_group_a = target_group_a
        self.target_group_b = target_group_b
        self.urgency = urgency

    def run(self) -> Optional[Codelet]:
        confidence_of_correspondence = self._calculate_confidence()
        if (
            confidence_of_correspondence > self.CONFIDENCE_THRESHOLD
            or confidence_of_correspondence < 1 - self.CONFIDENCE_THRESHOLD
        ):
            self.perceptlet_type.boost_activation(
                confidence_of_correspondence, self.target_group_a.location
            )
            correspondence = self.bubble_chamber.add_correspondence(
                self.parent_space, self.target_group_a, self.target_group_b
            )
            self._engender_follow_up(correspondence, confidence_of_correspondence)
        return None

    def _calculate_confidence(self) -> float:
        """Returns a high value for groups labeled with a proximate concept."""
        return fuzzy.AND(
            self.target_group_a.has_label_in_space(self.parent_space),
            self.target_group_b.has_label_in_space(self.parent_space),
            fuzzy.OR(
                len(self._common_labels_in_space()) > 1,
                self.parent_space.proximity_between(
                    self.target_group_a, self.target_group_b
                ),
            ),
        )

    def _common_labels_in_space(self):
        return set.intersection(
            self.target_group_a.labels_in_space(self.parent_space),
            self.target_group_b.labels_in_space(self.parent_space),
        )

    def _engender_follow_up(
        self, correspondence: Correspondence, urgency: float
    ) -> Codelet:
        from homer.codelets.correspondence_labeler import CorrespondenceLabeler

        return CorrespondenceLabeler(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "correspondence-label"
            ),
            correspondence,
            urgency,
        )
