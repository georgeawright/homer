from abc import ABC

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

    @property
    def targets_dict(self):
        raise NotImplementedError

    @property
    def targets_collection(self):
        return self.bubble_chamber.new_structure_collection(
            *[structure for name, structure in self.targets_dict.items()]
        )

    # TODO: decide whether to implement fizzle or get rid of it

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
