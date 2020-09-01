from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelets.evaluators.label_evaluator import LabelEvaluator
from homer.codelets.selectors.group_label_selector import GroupLabelSelector


class GroupLabelEvaluator(LabelEvaluator):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        target_label: Perceptlet,
        urgency: float,
        parent_id: str,
    ):
        LabelEvaluator.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            target_type,
            target_label,
            urgency,
            parent_id,
        )

    def _engender_follow_up(self) -> GroupLabelSelector:
        return GroupLabelSelector(
            self.bubble_chamber,
            self.bubble_chamber.concept_space["group-label-selection"],
            self.target_type,
            self.bubble_chamber.workspace.groups.at(self.location).get_most_active(),
            self.urgency,
            self.codelet_id,
        )
