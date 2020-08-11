import uuid
from abc import ABC, abstractmethod

from homer.bubble_chamber import BubbleChamber


class Codelet(ABC):
    def __init__(self, bubble_chamber: BubbleChamber, parent_id: str):
        self.bubble_chamber = bubble_chamber
        self.codelet_id = "codelet_" + uuid.uuid4().hex
        self.parent_id = parent_id

    @abstractmethod
    def run(self):
        """Perform main task of the codelet"""
        pass
