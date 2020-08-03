from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.hyper_parameters import HyperParameters
from homer.perceptlets.group import Group


class CorrespondenceSuggester(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_group_a: Group,
        target_group_b: Group,
        urgency: float,
    ):
        self.bubble_chamber = bubble_chamber
        self.perceptlet_type = perceptlet_type
        self.target_group_a = target_group_a
        self.target_group_b = target_group_b
        self.urgency = urgency

    def run(self):
        space = self.target_group_a.get_random_label().parent_concept.parent_space
        if self.target_group_b.has_label_in_space(
            space
        ) and not self.target_group_a.has_correspondence(self.target_group_b, space):
            self.perceptlet_type.boost_activation(0.1, self.target_group_a.location)
            return self._engender_follow_up(space, self.urgency)
        return self._engender_alternative_follow_up()

    def _engender_follow_up(self, space: Concept, urgency: float):
        from homer.codelets.correspondence_builder import CorrespondenceBuilder

        return CorrespondenceBuilder(
            self.bubble_chamber,
            self.perceptlet_type,
            space,
            self.target_group_a,
            self.target_group_b,
            urgency,
        )

    def _engender_alternative_follow_up(self):
        return CorrespondenceSuggester(
            self.bubble_chamber,
            self.perceptlet_type,
            *self.bubble_chamber.get_random_groups(2),
            self.urgency
        )
