from abc import ABC, abstractmethod

from .codelet_result import CodeletResult
from .float_between_one_and_zero import FloatBetweenOneAndZero


class Codelet(ABC):
    """A unit of work to be carried out in the workspace."""

    def __init__(
        self, codelet_id: str, parent_id: str, urgency: FloatBetweenOneAndZero
    ):
        self.codelet_id = codelet_id
        self.parent_id = parent_id
        self.urgency = urgency
        self.target_structure = None
        self.child_codelets = []
        self.result = None

    @abstractmethod
    def run(self) -> CodeletResult:
        pass
