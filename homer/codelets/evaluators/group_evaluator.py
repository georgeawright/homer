from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator
from homer.concepts.perceptlet_type import PerceptletType
from homer.perceptlets import Group


class GroupEvaluator(Evaluator):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        challenger_one: Group,
        challenger_two: Group,
        urgency: float,
        parent_id: str,
    ):
        Evaluator.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            target_type,
            challenger_one,
            challenger_two,
            urgency,
            parent_id,
        )

    def _run_competition(self) -> float:
        # compare two groups
        # increase strength of the best
        # decrease strength of the worst
        pass
