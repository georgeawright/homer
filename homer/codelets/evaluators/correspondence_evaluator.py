from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.bubbles.perceptlets import Correspondence
from homer.codelets.evaluator import Evaluator


class CorrespondenceEvaluator(Evaluator):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        champion: Correspondence,
        challenger: Correspondence,
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
        return (
            self.champion.first_argument == self.challenger.first_argument
            and self.champion.second_argument == self.challenger.second_argument
            and self.champion.parent_concept == self.challenger.parent_concept
        )

    def _run_competition(self) -> float:
        connection_activations_difference = (
            self.champion.total_connection_activations()
            - self.challenger.total_connection_activations()
        )
        return self._difference_score(connection_activations_difference)
