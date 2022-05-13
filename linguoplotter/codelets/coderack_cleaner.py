import random
import statistics

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID


class CoderackCleaner(Codelet):
    """Judges the effectiveness of recently run codelets according to
    change in bubble chamber satisfaction and removes from the coderack
    instances of offending codelet types probabilistically."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        last_satisfaction_score: FloatBetweenOneAndZero,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.coderack = coderack
        self.last_satisfaction_score = last_satisfaction_score

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        last_satisfaction_score: FloatBetweenOneAndZero,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            coderack,
            last_satisfaction_score,
            urgency,
        )

    def run(self) -> CodeletResult:
        self.bubble_chamber.loggers["activity"].log(
            self, f"Coderack population size: {self.coderack.population_size}"
        )
        current_satisfaction_score = self.bubble_chamber.satisfaction
        change_in_satisfaction_score = (
            current_satisfaction_score - self.last_satisfaction_score
        )
        transposed_change_in_satisfaction_score = (
            change_in_satisfaction_score * 0.5
        ) + 0.5
        probability_of_codelet_deletion = 1 - statistics.fmean(
            [current_satisfaction_score, transposed_change_in_satisfaction_score]
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self, self.coderack.recently_run, "Recently run"
        )
        for codelet in list(self.coderack._codelets):
            if type(codelet) not in self.coderack.recently_run:
                continue
            probability_of_deleting_codelet = statistics.fmean(
                [probability_of_codelet_deletion, 1 - codelet.urgency]
            )
            if probability_of_deleting_codelet > random.random() and not isinstance(
                codelet, self.coderack.PROTECTED_CODELET_TYPES
            ):
                self.bubble_chamber.loggers["activity"].log(self, f"Deleting {codelet}")
                self.coderack.remove_codelet(codelet)
        self.coderack.recently_run = set()
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                self.bubble_chamber.satisfaction,
                self.follow_up_urgency(),
            )
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Coderack population size: {self.coderack.population_size}"
        )
        self.result = CodeletResult.FINISH
        self.bubble_chamber.loggers["activity"].log_follow_ups(self)
        self.bubble_chamber.loggers["activity"].log_result(self)

    def follow_up_urgency(self) -> FloatBetweenOneAndZero:
        urgency = (1 - self.bubble_chamber.satisfaction) * (
            1 - (1 / self.coderack.population_size)
        )
        if urgency > self.coderack.MINIMUM_CODELET_URGENCY:
            return urgency
        return self.coderack.MINIMUM_CODELET_URGENCY
