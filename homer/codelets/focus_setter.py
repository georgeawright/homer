from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection_keys import exigency


class FocusSetter(Codelet):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
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
        self._set_focus_view()
        self._engender_follow_up()
        self.bubble_chamber.loggers["activity"].log_follow_ups(self)
        self.bubble_chamber.loggers["activity"].log_result(self)
        return self.result

    def _set_focus_view(self):
        self.bubble_chamber.loggers["activity"].log(
            self, f"Current focus: {self.bubble_chamber.focus.view}"
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Focussedness: {self.bubble_chamber.focus.focussedness}"
        )
        try:
            target_view = self.bubble_chamber.production_views.get(
                key=exigency, exclude=[self.bubble_chamber.focus.view]
            )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found target view: {target_view}"
            )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Target view exigency: {target_view.exigency}"
            )
        except MissingStructureError:
            self.result = CodeletResult.FIZZLE
            return
        if (
            self.bubble_chamber.focus.view is None
            or self.bubble_chamber.focus.view.unhappiness == 0
            or target_view.exigency > self.bubble_chamber.focus.focussedness
        ):
            self.bubble_chamber.focus.view = target_view
            self.bubble_chamber.loggers["activity"].log(
                self, f"Set focus: {target_view}"
            )
            self.result = CodeletResult.FINISH
        else:
            self.bubble_chamber.loggers["activity"].log(
                self, f"Focus unchanged: {self.bubble_chamber.focus.view}"
            )
            self.result = CodeletResult.FIZZLE

    def _engender_follow_up(self):
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                self.follow_up_urgency(),
            )
        )

    def follow_up_urgency(self) -> FloatBetweenOneAndZero:
        urgency = 1 - self.bubble_chamber.focus.focussedness
        if urgency > self.coderack.MINIMUM_CODELET_URGENCY:
            return urgency
        return self.coderack.MINIMUM_CODELET_URGENCY
