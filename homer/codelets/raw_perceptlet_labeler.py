from __future__ import annotations
from typing import Optional

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.perceptlet import Perceptlet


class RawPerceptletLabeler(Codelet):
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

    def _passes_preliminary_checks(self) -> bool:
        return not self.target_perceptlet.has_label(self.parent_concept)

    def _fizzle(self):
        self.perceptlet_type.decay_activation(self.target_perceptlet.location)
        return None

    def _calculate_confidence(self):
        proximity = self.parent_concept.proximity_to(
            self.target_perceptlet.get_value(self.parent_concept)
        )
        neighbours = self.target_perceptlet.proportion_of_neighbours_with_label(
            self.parent_concept
        )
        self.confidence = fuzzy.OR(proximity, neighbours)

    def _process_perceptlet(self):
        label = self.bubble_chamber.create_label(
            self.parent_concept,
            self.target_perceptlet.location,
            self.confidence,
            self.codelet_id,
        )
        self.target_perceptlet.add_label(label)

    def _engender_follow_up(self) -> RawPerceptletLabeler:
        new_target = self.target_perceptlet.most_exigent_neighbour()
        return RawPerceptletLabeler(
            self.bubble_chamber,
            self.perceptlet_type,
            self.parent_concept,
            new_target,
            self.confidence,
            self.codelet_id,
        )
