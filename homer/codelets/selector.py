from abc import abstractmethod
from typing import Union

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelet import Codelet
from homer.hyper_parameters import HyperParameters


class Selector(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.EVALUATOR_CONFIDENCE_THRESHOLD

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
        self.confidence = self._run_competition()

    def _process_perceptlet(self):
        self.champion.boost_activation(self.confidence)
        self.challenger.decay_activation(self.confidence)
        self.target_type.activation.decay(self.location)
        if abs(self.confidence) > 0:
            self.bubble_chamber.concept_space["satisfaction"].activation.boost(
                abs(self.confidence), self.location
            )

    @abstractmethod
    def _run_competition(self) -> float:
        pass

    def _difference_score(self, difference: Union[float, int]):
        score = 1 - 1 / (1 + abs(difference))
        return score if difference > 0 else -score
