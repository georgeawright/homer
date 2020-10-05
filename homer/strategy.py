from abc import ABC, abstractmethod

from .bubble_chamber import BubbleChamber


class Strategy(ABC):
    def __init__(self, bubble_chamber: BubbleChamber):
        self.bubble_chamber = bubble_chamber

    @abstractmethod
    @property
    def concept(self):
        pass
