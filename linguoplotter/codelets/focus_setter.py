from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection_keys import exigency
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
        targets = bubble_chamber.new_dict()
        return cls(codelet_id, parent_id, bubble_chamber, coderack, targets, urgency)

    def run(self) -> CodeletResult:
        try:
            if (
                self.bubble_chamber.worldview.view is not None
                and self.bubble_chamber.worldview.view.secondary_frames.filter(
                    lambda x: x.number_of_items_left_to_process > 0
                ).not_empty
            ):
                target_view = self.bubble_chamber.worldview.view
            else:
                target_view = self.bubble_chamber.views.filter(
                    lambda v: v.unhappiness > self.FLOATING_POINT_TOLERANCE
                    or v.secondary_frames.filter(
                        lambda f: f.number_of_items_left_to_process > 0
                    ).not_empty
                    and v.members.filter(
                        lambda c: c.parent_concept.name == "not(same)"
                    ).is_empty
                ).get(key=exigency)
            self.bubble_chamber.focus.view = target_view
            self.bubble_chamber.focus.frame = (
                target_view.parent_frame
                if target_view.secondary_frames.is_empty
                else target_view.secondary_frames.filter(
                    lambda x: x.number_of_items_left_to_process > 0
                ).get(key=exigency)
            )
            self.bubble_chamber.focus.recalculate_satisfaction()
            self.bubble_chamber.loggers["activity"].log(
                "Set focus\n"
                + f"View: {target_view}\n"
                + f"Frame: {self.bubble_chamber.focus.frame}\n"
                + f"Exigency: {target_view.exigency}\n"
                + f"Satisfaction: {self.bubble_chamber.focus.satisfaction}"
            )
            self._update_codelet_urgencies()
            self._engender_follow_up()
            self.result = CodeletResult.FINISH
        except MissingStructureError:
            self.result = CodeletResult.FIZZLE
            self._fizzle()
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
