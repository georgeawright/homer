from abc import ABC

from .bubble_chamber import BubbleChamber
from .codelet_result import CodeletResult
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters
from .structure_collections import StructureSet


class Codelet(ABC):
    """A unit of work to be carried out in the bubble chamber."""

    FLOATING_POINT_TOLERANCE = HyperParameters.FLOATING_POINT_TOLERANCE
    MINIMUM_CODELET_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY

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
        self.result = None

    @classmethod
    def get_target_class(cls):
        raise NotImplementedError

    def run(self) -> CodeletResult:
        raise NotImplementedError

    def __repr__(self) -> str:
        if self.result is None:
            return f"<{self.codelet_id} (urgency: {self.urgency})>"
        else:
            return f"<{self.codelet_id} (result: {self.result})>"
