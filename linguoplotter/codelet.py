from abc import ABC

from .bubble_chamber import BubbleChamber
from .codelet_result import CodeletResult
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters
from .structure_collections import StructureSet


class Codelet(ABC):
    """A unit of work to be carried out in the bubble chamber."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureSet,
        urgency: FloatBetweenOneAndZero,
    ):
        self.codelet_id = codelet_id
        self.parent_id = parent_id
        self.bubble_chamber = bubble_chamber
        self.targets = targets
        self.urgency = urgency
        self.child_codelets = []
        self.child_structures = None
        self.result = CodeletResult.FAIL
        self.FLOATING_POINT_TOLERANCE = (
            self.bubble_chamber.hyper_parameters.FLOATING_POINT_TOLERANCE
        )
        self.MINIMUM_CODELET_URGENCY = (
            self.bubble_chamber.hyper_parameters.MINIMUM_CODELET_URGENCY
        )

    @classmethod
    def get_target_class(cls):
        raise NotImplementedError

    def run(self) -> CodeletResult:
        raise NotImplementedError

    def adjust_urgency(self, amount: FloatBetweenOneAndZero) -> None:
        new_urgency = FloatBetweenOneAndZero(self.urgency + amount)
        self.bubble_chamber.loggers["activity"].log(
            f"Adjusting {self.codelet_id} urgency from {self.urgency} to {new_urgency}"
        )
        self.urgency = new_urgency

    def __repr__(self) -> str:
        if self.result is None:
            return f"<{self.codelet_id} (urgency: {self.urgency})>"
        else:
            return f"<{self.codelet_id} (result: {self.result})>"
