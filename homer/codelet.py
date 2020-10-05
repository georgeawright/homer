from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from .bubble_chamber import BubbleChamber
from .hyper_parameters import HyperParameters


class Codelet(ABC):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        urgency: float,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
    ):
        self.urgency = urgency
        self.codelet_id = codelet_id
        self.parent_id = parent_id
        self.bubble_chamber = bubble_chamber
        self.child_codelets = []

    @classmethod
    @abstractmethod
    def from_components(cls) -> Codelet:
        pass

    @abstractmethod
    def run(self) -> Optional[Codelet]:
        pass
