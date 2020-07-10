from abc import ABC, abstractmethod

from homer.bubble_chamber import BubbleChamber


class Codelet(ABC):
    def __init__(self, bubble_chamber: BubbleChamber):
        self.bubble_chamber = bubble_chamber

    @abstractmethod
    def run(self):
        """Perform main task of the codelet"""
        pass
