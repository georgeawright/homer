from __future__ import annotations
import statistics
from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.bubbles.perceptlets import Group, Label
from homer.codelets.bottom_up_raw_perceptlet_labeler import BottomUpRawPerceptletLabeler
from homer.codelets.evaluator import Evaluator
from homer.errors import MissingPerceptletError


class GroupLabelEvaluator(Evaluator):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        target_group: Group,
        urgency: float,
        parent_id: str,
        champion: Optional[Label] = None,
        challenger: Optional[Label] = None,
    ):
        Evaluator.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            target_type,
            target_group,
            urgency,
            parent_id,
        )
        self.target_group = target_group
        self.champion = champion
        self.challenger = challenger

    def _passes_preliminary_checks(self) -> bool:
        if self.champion is None:
            try:
                self.champion = self.target_group.labels.get_most_active()
            except MissingPerceptletError:
                return False
        if self.challenger is None:
            try:
                self.challenger = self.target_group.labels.get_random()
            except MissingPerceptletError:
                return False
        if self.challenger == self.champion:
            return False
        if self.champion.parent_concept.space != self.challenger.parent_concept.space:
            return False
        self.target_space = self.champion.parent_concept.space
        self.champion_proportion = self.target_group.members.proportion_with_label(
            self.champion.parent_concept
        )
        self.challenger_proportion = self.target_group.members.proportion_with_label(
            self.challenger.parent_concept
        )
        return (
            self.champion_proportion > self.CONFIDENCE_THRESHOLD
            and self.challenger_proportion > self.CONFIDENCE_THRESHOLD
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

    def _engender_follow_up(self) -> GroupLabelEvaluator:
        winner, loser = (
            (self.champion, self.challenger)
            if self.champion.activation.as_scalar()
            > self.challenger.activation.as_scalar()
            else (self.challenger, self.champion)
        )
        return GroupLabelEvaluator(
            self.bubble_chamber,
            self.perceptlet_type,
            self.target_type,
            self.target_group,
            loser.exigency,
            self.codelet_id,
            champion=winner,
            challenger=loser,
        )
