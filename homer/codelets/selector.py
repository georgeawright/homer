from __future__ import annotations
import random
import statistics
from typing import Union

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.codelet import Codelet
from homer.errors import MissingPerceptletError
from homer.hyper_parameters import HyperParameters
from homer.perceptlet_collection import PerceptletCollection


class Selector(Codelet):

    SELECTION_RANDOMNESS = HyperParameters.SELECTION_RANDOMNESS

    def __init__(
        self,
        urgency: float,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Perceptlet,
        challenger: Union[Perceptlet, None],
        parent_perceptlet_type: type,
    ):
        Codelet.__init__(
            self, urgency, codelet_id, parent_id, bubble_chamber,
        )
        self.champion = champion
        self.challenger = challenger
        self.parent_perceptlet_type = None

    @classmethod
    def from_components(
        cls,
        urgency: float = None,
        parent_id: str = None,
        target_perceptlet: Perceptlet = None,
        target_perceptlet_type: type = None,
        parent_perceptlet_type: type = None,
    ) -> Selector:
        codelet_id = None
        champion = (
            PerceptletCollection.union(
                PerceptletCollection(target_perceptlet), target_perceptlet.neighbours
            ).get_most_active()
            if target_perceptlet is not None
            else target_perceptlet_type.instances.get_most_active()
        )
        challenger = (
            target_perceptlet
            if target_perceptlet is not None and champion != target_perceptlet
            else None
        )
        return Selector(
            urgency, codelet_id, parent_id, champion, challenger, parent_perceptlet_type
        )

    def run(self):
        while self.challenger is None:
            try:
                self.challenger = self.champion.neighbours.get_random()
            except MissingPerceptletError:
                from .builder import Builder

                self.child_codelets.append(
                    Builder.from_components(
                        parent_id=self.codelet_id,
                        target_perceptlet_type=self.parent_perceptlet_type,
                        child_perceptlet_type=type(self.champion),
                    )
                )
                return
        champion_score = (
            self.champion.quality * (1 - self.SELECTION_RANDOMNESS)
            + random.random() * self.SELECTION_RANDOMNESS
        )
        challenger_score = (
            self.challenger.quality * (1 - self.SELECTION_RANDOMNESS)
            + random.random() * self.SELECTION_RANDOMNESS
        )
        self.confidence = champion_score - challenger_score
        self.champion.boost_activation(self.confidence)
        self.challenger.decay_activation(self.confidence)
        self.bubble_chamber.logger.log_perceptlet_update(
            self, self.champion, "Activation updated"
        )
        self.bubble_chamber.logger.log_perceptlet_update(
            self, self.challenger, "Activation updated"
        )
        satisfaction = statistics.fmean(
            [
                self.champion.activation.as_scalar() * self.champion.quality,
                self.challenger.activation.as_scalar() * self.challenger.quality,
            ]
        )
        self.bubble_chamber.concept_space["satisfaction"].activation.boost(
            satisfaction, self.location
        )
