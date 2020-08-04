from typing import Optional

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concepts.perceptlet_type import PerceptletType
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet

from homer.codelets.group_labeler import GroupLabeler
from homer.perceptlets.group import Group


class GroupBuilder(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_perceptlet: Optional[Perceptlet],
        urgency: float,
    ):
        Codelet.__init__(self, bubble_chamber)
        self.perceptlet_type = perceptlet_type
        self.target_perceptlet = target_perceptlet
        self.urgency = urgency

    def run(self) -> Optional[Codelet]:
        neighbour = self.target_perceptlet.get_random_neighbour()
        confidence_of_group_affinity = self._calculate_confidence(
            self.target_perceptlet, neighbour
        )
        if confidence_of_group_affinity > self.CONFIDENCE_THRESHOLD:
            self.perceptlet_type.boost_activation(
                confidence_of_group_affinity, self.target_perceptlet.location
            )
            group = self.bubble_chamber.create_group(
                {self.target_perceptlet, neighbour}, confidence_of_group_affinity
            )
            self.target_perceptlet.add_group(group)
            neighbour.add_group(group)
            print(
                f"GROUP BUILT: {self.target_perceptlet.value} at {self.target_perceptlet.location} and {neighbour.value} at {neighbour.location}, confidence: {group.strength}"
            )
            return self._engender_follow_up(group, confidence_of_group_affinity)
        return None

    def _calculate_confidence(
        self, perceptlet_a: Perceptlet, perceptlet_b: Perceptlet,
    ) -> float:
        common_concepts = set.intersection(
            {label.parent_concept for label in perceptlet_a.labels},
            {label.parent_concept for label in perceptlet_b.labels},
        )
        distances = [
            concept.proximity_between(
                perceptlet_a.get_value(concept), perceptlet_b.get_value(concept),
            )
            for concept in common_concepts
        ]
        if distances == []:
            return 0.0
        return fuzzy.OR(*distances)

    def _engender_follow_up(self, group: Group, confidence: float) -> Codelet:
        return GroupLabeler(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "group-label"
            ),
            group,
            confidence,
        )
