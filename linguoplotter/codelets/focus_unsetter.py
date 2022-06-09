import statistics

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID


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
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.coderack = coderack
        self.last_satisfaction_score = last_satisfaction_score
        self.target_view = self.bubble_chamber.focus.view
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
        current_satisfaction_score = self.bubble_chamber.satisfaction
        change_in_satisfaction_score = (
            current_satisfaction_score - self.last_satisfaction_score
        )
        transposed_change_in_satisfaction_score = (
            change_in_satisfaction_score * 0.5
        ) + 0.5
        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Current bubble chamber satisfaction: {self.bubble_chamber.satisfaction}",
        )
        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Change in satisfaction: {change_in_satisfaction_score}",
        )
        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Transposed change in satisfaction: {transposed_change_in_satisfaction_score}",
        )
        if self.bubble_chamber.focus.view.unhappiness == 0.0:
            probability_of_unsetting_focus = 1
            self._update_worldview_setter_urgency()
        else:
            probability_of_unsetting_focus = statistics.fmean(
                [
                    current_satisfaction_score,
                    transposed_change_in_satisfaction_score,
                ]
            )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Probability of unsetting focus: {probability_of_unsetting_focus}"
        )
        random_number = self.bubble_chamber.random_machine.generate_number()
        self.bubble_chamber.loggers["activity"].log(
            self, f"Random number: {random_number}"
        )
        if random_number > probability_of_unsetting_focus:
            self.bubble_chamber.loggers["activity"].log(self, "Focus left set.")
            self.result = CodeletResult.FIZZLE
            self._fizzle()
        else:
            if transposed_change_in_satisfaction_score <= 0.5:
                self.bubble_chamber.loggers["activity"].log(self, "Decaying focus")
                self.bubble_chamber.focus.view._activation == 0
            self.bubble_chamber.focus.view = None
            self.bubble_chamber.loggers["activity"].log(self, "Focus unset.")
            self._engender_follow_up()
            self.result = CodeletResult.FINISH
        self.bubble_chamber.loggers["activity"].log_follow_ups(self)
        self.bubble_chamber.loggers["activity"].log_result(self)
        return self.result

    def _update_worldview_setter_urgency(self):
        for codelet in self.coderack._codelets:
            if "WorldviewSetter" in codelet.codelet_id:
                codelet.urgency = self.bubble_chamber.focus.satisfaction
                return
        raise Exception

    def _fizzle(self):
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                self.bubble_chamber.satisfaction,
                0.5,
            )
        )

    def _engender_follow_up(self):
        from linguoplotter.codelets import FocusSetter
        from linguoplotter.codelets.evaluators.view_evaluators import (
            SimplexViewEvaluator,
        )

        self.child_codelets.append(
            FocusSetter.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                0.5,
            )
        )
        self.child_codelets.append(
            SimplexViewEvaluator.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.bubble_chamber.new_structure_collection(self.target_view),
                1.0,
            )
        )
