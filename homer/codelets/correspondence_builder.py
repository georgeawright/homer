from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.perceptlets.group import Group


class CorrespondenceBuilder(Codelet):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        parent_concept: Concept,
        target_group_a: Group,
        target_group_b: Group,
        urgency: float,
        parent_id: str,
    ):
        Codelet.__init__(self, bubble_chamber, parent_id)
        self.perceptlet_type = perceptlet_type
        self.parent_concept = parent_concept
        self.target_perceptlet = target_group_a
        self.second_target_perceptlet = target_group_b
        self.urgency = urgency

    def _passes_preliminary_checks(self) -> bool:
        return True

    def _fizzle(self):
        self.perceptlet_type.decay_activation(self.target_perceptlet.location)
        return None

    def _calculate_confidence(self):
        self.confidence = max(
            self._confidence_of_proximity(), 1 - self._confidence_of_proximity()
        )

    def _confidence_of_proximity(self) -> float:
        """Returns a high value for groups labeled with a proximate concept."""
        return fuzzy.AND(
            self.target_perceptlet.has_label_in_space(self.parent_concept),
            self.second_target_perceptlet.has_label_in_space(self.parent_concept),
            fuzzy.OR(
                len(self._common_labels_in_space()) > 1,
                self.parent_concept.proximity_between(
                    self.target_perceptlet.get_value(self.parent_concept),
                    self.second_target_perceptlet.get_value(self.parent_concept),
                ),
            ),
        )

    def _common_labels_in_space(self):
        return set.intersection(
            self.target_perceptlet.labels_in_space(self.parent_concept),
            self.second_target_perceptlet.labels_in_space(self.parent_concept),
        )

    def _process_perceptlet(self):
        self.correspondence = self.bubble_chamber.create_correspondence(
            "correspondence",
            self.parent_concept,
            self.target_perceptlet,
            self.second_target_perceptlet,
            self.confidence,
            self.codelet_id,
        )
        self.target_perceptlet.add_correspondence(self.correspondence)

    def _engender_follow_up(self):
        from homer.codelets.correspondence_labeler import CorrespondenceLabeler

        return CorrespondenceLabeler(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "correspondence-label"
            ),
            self.parent_concept,
            self.correspondence,
            self.confidence,
            self.codelet_id,
        )
