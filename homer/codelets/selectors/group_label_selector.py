from __future__ import annotations
from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.bubbles.perceptlets import Group, Label
from homer.codelets.bottom_up_raw_perceptlet_labeler import BottomUpRawPerceptletLabeler
from homer.codelets.selector import Selector
from homer.errors import MissingPerceptletError


class GroupLabelSelector(Selector):
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
        Selector.__init__(
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
        self.perceptlet_type.activation.decay(self.location)
        return BottomUpRawPerceptletLabeler(
            self.bubble_chamber,
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name("label"),
            self.target_group.members.get_unhappy(),
            self.urgency,
            self.codelet_id,
        )

    def _engender_follow_up(self) -> GroupLabelSelector:
        winner, loser = (
            (self.champion, self.challenger)
            if self.champion.activation.as_scalar()
            > self.challenger.activation.as_scalar()
            else (self.challenger, self.champion)
        )
        return GroupLabelSelector(
            self.bubble_chamber,
            self.perceptlet_type,
            self.target_type,
            self.target_group,
            loser.exigency,
            self.codelet_id,
            champion=winner,
            challenger=loser,
        )
