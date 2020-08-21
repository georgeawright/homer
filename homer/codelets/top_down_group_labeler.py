from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Concept
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.bubbles.perceptlets import Group
from homer.codelet import Codelet

from .group_extender import GroupExtender
from .raw_perceptlet_labeler import RawPerceptletLabeler


class TopDownGroupLabeler(Codelet):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        parent_concept: Concept,
        target_group: Group,
        urgency: float,
        parent_id: str,
    ):
        Codelet.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            parent_concept,
            target_group,
            urgency,
            parent_id,
        )

    def _passes_preliminary_checks(self) -> bool:
        return not self.target_perceptlet.has_label(self.parent_concept)

    def _fizzle(self):
        self.perceptlet_type.decay_activation(self.target_perceptlet.location)
        return None

    def _fail(self) -> RawPerceptletLabeler:
        self.perceptlet_type.decay_activation(self.target_perceptlet.location)
        return RawPerceptletLabeler(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name("label"),
            self.parent_concept,
            self.target_perceptlet.members.get_unhappy(),
            self.urgency,
            self.codelet_id,
        )

    def _calculate_confidence(self):
        total_strength = 0.0
        for member in self.target_perceptlet.members:
            for label in member.labels:
                if label.parent_concept == self.parent_concept:
                    total_strength += label.strength
        self.confidence = total_strength / self.target_perceptlet.size

    def _process_perceptlet(self):
        label = self.bubble_chamber.create_label(
            self.parent_concept,
            self.target_perceptlet.location,
            self.confidence,
            self.codelet_id,
        )
        self.target_perceptlet.labels.add(label)

    def _engender_follow_up(self) -> GroupExtender:
        return GroupExtender(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name("group"),
            self.target_perceptlet,
            self.confidence,
            self.codelet_id,
        )
