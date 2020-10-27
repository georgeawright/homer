from abc import ABC, abstractmethod

from homer.float_between_zero_and_one import FloatBetweenZeroAndOne


class Codelet(ABC):
    """A unit of work to be carried out in the workspace."""

    def __init__(
        self, codelet_id: str, parent_id: str, urgency: FloatBetweenZeroAndOne
    ):
        self.codelet_id = codelet_id
        self.parent_id = parent_id
        self.urgency = urgency
        self.child_codelets = []

    @abstractmethod
    def run(self):
        pass
