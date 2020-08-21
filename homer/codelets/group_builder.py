from typing import Optional

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelet import Codelet
from homer.errors import MissingPerceptletError
from homer.perceptlet_collection import PerceptletCollection

from .group_labeler import GroupLabeler


class GroupBuilder(Codelet):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_perceptlet: Optional[Perceptlet],
        urgency: float,
        parent_id: str,
    ):
        parent_concept = None
        Codelet.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            parent_concept,
            target_perceptlet,
            urgency,
            parent_id,
        )

    def _passes_preliminary_checks(self) -> bool:
        try:
            self.second_target_perceptlet = (
                self.target_perceptlet.neighbours.get_random()
            )
        except MissingPerceptletError:
            return False
        if self.target_perceptlet.makes_group_with(
            PerceptletCollection({self.second_target_perceptlet})
        ):
            return False
        return True

    def _fizzle(self):
        return self._fail()

    def _fail(self):
        self._decay_concept(self.perceptlet_type)
        return None

    def _calculate_confidence(self):
        common_concepts = set.intersection(
            {label.parent_concept for label in self.target_perceptlet.labels},
            {label.parent_concept for label in self.second_target_perceptlet.labels},
        )
        distances = [
            concept.proximity_between(
                self.target_perceptlet.get_value(concept),
                self.second_target_perceptlet.get_value(concept),
            )
            for concept in common_concepts
        ]
        self.confidence = 0.0 if distances == [] else fuzzy.OR(*distances)

    def _process_perceptlet(self):
        self.group = self.bubble_chamber.create_group(
            PerceptletCollection(
                {self.target_perceptlet, self.second_target_perceptlet}
            ),
            self.confidence,
            self.codelet_id,
        )
        self.target_perceptlet.groups.add(self.group)
        self.second_target_perceptlet.groups.add(self.group)

    def _engender_follow_up(self) -> GroupLabeler:
        return GroupLabeler(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "group-label"
            ),
            self.group,
            self.confidence,
            self.codelet_id,
        )
