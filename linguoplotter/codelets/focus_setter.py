from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict


class FocusSetter(Codelet):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, targets, urgency)
        self.coderack = coderack

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        targets = bubble_chamber.new_dict()
        return cls(codelet_id, parent_id, bubble_chamber, coderack, targets, urgency)

    def run(self) -> CodeletResult:
        try:
            target_view = self.bubble_chamber.views.filter(
                lambda v: (v.unhappiness > 0)
                and v.members.filter(
                    lambda c: c.parent_concept.name == "not(same)"
                ).is_empty
            ).get(key=lambda x: fuzzy.AND(x.salience, 1 - 1 / x.parent_frame.depth))
            self.bubble_chamber.focus.frame = target_view.parent_frame
            self.bubble_chamber.focus.view = target_view
            self.bubble_chamber.loggers["activity"].log(
                "Set focus\n"
                + f"View: {target_view}\n"
                + f"Frame: {self.bubble_chamber.focus.frame}"
            )
            self.bubble_chamber.focus.recalculate_satisfaction()
            self.bubble_chamber.loggers["activity"].log(
                f"Salience: {target_view.salience}\n"
                + f"Satisfaction: {self.bubble_chamber.focus.satisfaction}"
            )
            self._update_codelet_urgencies(target_view.salience)
            self._engender_follow_up()
            self.result = CodeletResult.FINISH
        except MissingStructureError:
            self.bubble_chamber.loggers["activity"].log("No view and frame found.")
            self.result = CodeletResult.FIZZLE
            self._fizzle()
        self.bubble_chamber.focus_setters_since_last_successful_focus_unset += 1
        return self.result

    def _update_codelet_urgencies(self, amount: FloatBetweenOneAndZero):
        for codelet in self.coderack._codelets:
            if "ViewDrivenFactory" in codelet.codelet_id:
                codelet.adjust_urgency(amount)
                return
        raise Exception

    def _fizzle(self):
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                self.coderack.MINIMUM_CODELET_URGENCY,
            )
        )

    def _engender_follow_up(self):
        from linguoplotter.codelets import FocusUnsetter

        self.child_codelets.append(
            FocusUnsetter.spawn(
                parent_id=self.codelet_id,
                bubble_chamber=self.bubble_chamber,
                coderack=self.coderack,
                last_satisfaction_score=self.bubble_chamber.focus.satisfaction,
                time_focus_set=self.coderack.codelets_run,
                urgency=0.5,
            )
        )

    def follow_up_urgency(self) -> FloatBetweenOneAndZero:
        urgency = 1 - self.bubble_chamber.focus.view.salience
        if urgency > self.coderack.MINIMUM_CODELET_URGENCY:
            return urgency
        return self.coderack.MINIMUM_CODELET_URGENCY
