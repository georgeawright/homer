from __future__ import annotations
import statistics

from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.bubbles.perceptlets import Group
from homer.codelets.evaluator import Evaluator
from homer.hyper_parameters import HyperParameters
from homer.perceptlet_collection import PerceptletCollection


class GroupEvaluator(Evaluator):

    PROPORTION_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        champion: Group,
        challenger: Group,
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

    def _passes_preliminary_checks(self) -> bool:
        shared_members = PerceptletCollection.union(
            self.champion.members, self.challenger.members
        )
        shared_champion_ratio = len(shared_members) / len(self.champion.members)
        shared_challenger_ratio = len(shared_members) / len(self.challenger.members)
        return (
            shared_champion_ratio > self.PROPORTION_THRESHOLD
            and shared_challenger_ratio > self.PROPORTION_THRESHOLD
        )

    def _run_competition(self) -> float:
        size_difference = self.champion.size - self.challenger.size
        connection_activations_difference = (
            self.champion.total_connection_activations()
            - self.challenger.total_connection_activations()
        )
        return statistics.fmean(
            [
                self._difference_score(size_difference),
                self._difference_score(connection_activations_difference),
            ]
        )

    def _engender_follow_up(self) -> GroupEvaluator:
        winner, loser = (
            (self.champion, self.challenger)
            if self.champion.activation.as_scalar()
            > self.challenger.activation.as_scalar()
            else (self.challenger, self.champion)
        )
        return GroupEvaluator(
            self.bubble_chamber,
            self.perceptlet_type,
            self.target_type,
            winner,
            loser,
            1 - abs(self.confidence),
            self.codelet_id,
        )
