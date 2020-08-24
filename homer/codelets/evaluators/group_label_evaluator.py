import statistics

from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.bubbles.perceptlets import Group, Label
from homer.codelets.bottom_up_raw_perceptlet_labeler import BottomUpRawPerceptletLabeler
from homer.codelets.evaluator import Evaluator


class GroupLabelEvaluator(Evaluator):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        target_group: Group,
        champion: Label,
        challenger: Label,
        urgency: float,
        parent_id: str,
    ):
        Evaluator.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            target_type,
            champion,
            challenger,
            urgency,
            parent_id,
        )
        self.target_group = target_group
        self.target_space = champion.parent_concept.space

    def _passes_preliminary_checks(self) -> bool:
        self.champion_proportion = self.target_group.members.proportion_with_label(
            self.champion
        )
        self.challenger_proportion = self.target_group.members.proportion_with_label(
            self.challenger
        )
        return (
            self.champion_proportion > self.CONFIDENCE_THRESHOLD
            and self.challenger.proportion > self.CONFIDENCE_THRESHOLD
        )

    def _fizzle(self) -> BottomUpRawPerceptletLabeler:
        return BottomUpRawPerceptletLabeler(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name("label"),
            self.target_group.members.get_unhappy(),
            self.urgency,
            self.codelet_id,
        )

    def _run_competition(self) -> float:
        champion_proximity = self.champion.parent_concept.proximity_to(
            self.target_group.get_value(self.target_space)
        )
        challenger_proximity = self.challenger.parent_concept.proximity_to(
            self.target_group.get_value(self.target_space)
        )
        proximity_difference = champion_proximity - challenger_proximity
        proportion_with_label_difference = (
            self.champion_proportion - self.challenger_proportion
        )
        return statistics.fmean(
            [proximity_difference, proportion_with_label_difference]
        )
