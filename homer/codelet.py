from abc import ABC, abstractmethod


class Codelet(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self):
        """Perform main task of the codelet"""
        pass
