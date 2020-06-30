from abc import ABC, abstractmethod
from typing import Any


class ConceptNode(ABC):
    def __init__(self, name: str, depth: float, prototype: Any, activation: float):
        self.name = name
        self.depth = depth
        self.prototype = prototype
        self.activation = activation

    @abstractmethod
    def distance_from(self, candidate_instance: Any) -> float:
        """Return distance from prototype to candidate instance."""
        pass
