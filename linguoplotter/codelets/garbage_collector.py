from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.hyper_parameters import HyperParameters


class GarbageCollector(Codelet):

    MINIMUM_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY

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

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            coderack,
            urgency,
        )

    def run(self) -> CodeletResult:
        if self.bubble_chamber.recycle_bin.is_empty:
            self.result = CodeletResult.FIZZLE
        else:
            self._remove_items()
            self.result = CodeletResult.FINISH
        self._engender_follow_up()
        self.bubble_chamber.loggers["activity"].log_follow_ups(self)
        self.bubble_chamber.loggers["activity"].log_result(self)
        return self.result

    def _remove_items(self):
        for structure in self.bubble_chamber.recycle_bin:
            if not structure.is_recyclable:
                self.bubble_chamber.recycle_bin.remove(structure)
                continue
            if any(
                [
                    structure in codelet.target_structures
                    or (
                        hasattr(codelet, "target_view")
                        and codelet.target_view is not None
                        and structure in codelet.target_view.structures
                    )
                    for codelet in self.coderack._codelets
                ]
            ):
                self.bubble_chamber.recycle_bin.remove(structure)
                continue
            probability_of_removal = (
                self.bubble_chamber.random_machine.generate_number()
            )
            if probability_of_removal > self.bubble_chamber.general_satisfaction:
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Removing {structure}"
                )
                self.bubble_chamber.recycle_bin.remove(structure)
                self.bubble_chamber.remove(structure)

    def _engender_follow_up(self):
        urgency = max(
            min(1, self.MINIMUM_URGENCY * len(self.bubble_chamber.recycle_bin)),
            self.MINIMUM_URGENCY,
        )
        self.child_codelets.append(
            self.spawn(self.codelet_id, self.bubble_chamber, self.coderack, urgency)
        )
