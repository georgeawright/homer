from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection_keys import exigency


class FocusSetter(Codelet):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.coderack = coderack
        self.result = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, coderack, urgency)

    def run(self) -> CodeletResult:
        try:
            target_view = self.bubble_chamber.views.filter(
                lambda x: x.unhappiness > 0
            ).get(key=exigency)
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found target view: {target_view}"
            )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Target view exigency: {target_view.exigency}"
            )
            self.bubble_chamber.focus.view = target_view
            self.bubble_chamber.loggers["activity"].log(
                self, f"Set focus: {target_view}"
            )
            self.bubble_chamber.focus.recalculate_satisfaction()
            self.bubble_chamber.loggers["activity"].log(
                self, f"Focus satisfaction: {self.bubble_chamber.focus.satisfaction}"
            )
            self._update_codelet_urgencies()
            self._engender_follow_up()
            self.result = CodeletResult.FINISH
        except MissingStructureError:
            self.result = CodeletResult.FIZZLE
            self._fizzle()
        self.bubble_chamber.loggers["activity"].log_follow_ups(self)
        self.bubble_chamber.loggers["activity"].log_result(self)
        return self.result

    def _update_codelet_urgencies(self):
        for codelet in self.coderack._codelets:
            if "ViewDrivenFactory" in codelet.codelet_id:
                codelet.urgency = 1.0
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
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                self.bubble_chamber.focus.satisfaction,
                0.5,
            )
        )

    def follow_up_urgency(self) -> FloatBetweenOneAndZero:
        urgency = 1 - self.bubble_chamber.focus.view.exigency
        if urgency > self.coderack.MINIMUM_CODELET_URGENCY:
            return urgency
        return self.coderack.MINIMUM_CODELET_URGENCY
