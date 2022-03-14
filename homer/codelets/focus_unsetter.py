import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection_keys import exigency


class FocusUnsetter(Codelet):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        last_satisfaction_score: FloatBetweenOneAndZero,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.coderack = coderack
        self.last_satisfaction_score = last_satisfaction_score
        self.result = None

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
            self, f"Focus satisfaction: {self.bubble_chamber.focus.satisfaction}"
        )
        current_satisfaction_score = self.bubble_chamber.focus.satisfaction
        change_in_satisfaction_score = (
            current_satisfaction_score - self.last_satisfaction_score
        )
        transposed_change_in_satisfaction_score = (
            change_in_satisfaction_score * 0.5
        ) + 0.5
        probability_of_unsetting_focus = 1 - statistics.fmean(
            [current_satisfaction_score, transposed_change_in_satisfaction_score]
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Probability of unsetting focus: {probability_of_unsetting_focus}"
        )
        random_number = self.bubble_chamber.random_machine.generate_number()
        if random_number < probability_of_unsetting_focus:
            self.bubble_chamber.loggers["activity"].log(self, "Focus left set.")
            self.result = CodeletResult.FIZZLE
            self._fizzle()
        else:
            self.bubble_chamber.focus.view = None
            self.bubble_chamber.loggers["activity"].log(self, "Focus unset.")
            self._engender_follow_up()
            self.result = CodeletResult.FINISH
        self.bubble_chamber.loggers["activity"].log_result(self)
        return self.result

    def _fizzle(self):
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                self.bubble_chamber.satisfaction,
                self.bubble_chamber.satisfaction,
            )
        )

    def _engender_follow_up(self):
        from homer.codelets import FocusSetter

        self.child_codelets.append(
            FocusSetter.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                1 - self.bubble_chamber.satisfaction,
            )
        )
