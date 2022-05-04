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
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
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
            target_view = self.bubble_chamber.recycle_bin.remove_oldest()
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found target view: {target_view}"
            )
            other_codelet_target_views = [
                codelet.target_view if hasattr(codelet, "target_view") else None
                for codelet in self.coderack._codelets
            ]
            if (
                target_view in other_codelet_target_views
                or target_view.activation > 0.0
            ):
                self.result = CodeletResult.FIZZLE
            else:
                self.result = CodeletResult.FINISH
                for correspondence in target_view.members:
                    for argument in correspondence.arguments:
                        argument.links_out.remove(correspondence)
                        argument.links_in.remove(correspondence)
                        self.bubble_chamber.correspondences.remove(correspondence)
                        self.bubble_chamber.views.remove(target_view)
                        self.result = CodeletResult.FINISH
        self._engender_follow_up()
        self.bubble_chamber.loggers["activity"].log_result(self)
        return self.result

    def _engender_follow_up(self):
        urgency = max(
            min(1, self.MINIMUM_URGENCY * len(self.bubble_chamber.views)),
            self.MINIMUM_URGENCY,
        )
        self.child_codelets.append(
            self.spawn(self.codelet_id, self.bubble_chamber, self.coderack, urgency)
        )
