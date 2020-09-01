import random
import statistics

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelet import Codelet
from homer.hyper_parameters import HyperParameters


class Selector(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.EVALUATOR_CONFIDENCE_THRESHOLD
    SELECTION_RANDOMNESS = HyperParameters.SELECTION_RANDOMNESS

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        champion: Perceptlet,
        urgency: float,
        parent_id: str,
    ):
        parent_concept = None
        Codelet.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            parent_concept,
            champion,
            urgency,
            parent_id,
        )
        self.target_type = target_type
        self.champion = champion

    def _fizzle(self):
        self.perceptlet_type.activation.decay(self.location)
        return None

    def _fail(self):
        pass

    def _calculate_confidence(self):
        champion_score = (
            self.champion.quality * (1 - self.SELECTION_RANDOMNESS)
            + random.random() * self.SELECTION_RANDOMNESS
        )
        challenger_score = (
            self.challenger.quality * (1 - self.SELECTION_RANDOMNESS)
            + random.random() * self.SELECTION_RANDOMNESS
        )
        self.confidence = champion_score - challenger_score

    def _process_perceptlet(self):
        self.champion.boost_activation(self.confidence)
        self.challenger.decay_activation(self.confidence)
        self.target_type.activation.decay(self.location)
        satisfaction = statistics.fmean(
            [
                self.champion.activation.as_scalar() * self.champion.quality,
                self.challenger.activation.as_scalar() * self.challenger.quality,
            ]
        )
        self.bubble_chamber.concept_space["satisfaction"].activation.boost(
            satisfaction, self.location
        )
