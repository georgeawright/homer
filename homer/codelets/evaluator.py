from abc import abstractmethod

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concepts.perceptlet_type import PerceptletType
from homer.perceptlet import Perceptlet


class Evaluator(Codelet):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        challenger_one: Perceptlet,
        challenger_two: Perceptlet,
        urgency: float,
        parent_id: str,
    ):
        parent_concept = None
        Codelet.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            parent_concept,
            challenger_one,
            urgency,
            parent_id,
        )
        self.target_type = target_type
        self.challenger_one = challenger_one
        self.challenger_two = challenger_two

    def _passes_preliminary_checks(self) -> bool:
        return True

    def _fizzle(self):
        self.perceptlet_type.decay_activation(self.challenger_one.location)
        return None

    def _fail(self):
        pass

    def _calculate_confidence(self):
        self.confidence = self._run_competition()

    def _process_perceptlet(self):
        self.winner.strength += self.confidence
        self.loser.strength -= self.confidence

    def _engender_follow_up(self):
        pass

    @abstractmethod
    def _run_competition(self) -> float:
        pass
