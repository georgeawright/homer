from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from .hyper_parameters import HyperParameters


class Codelet(ABC):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self, urgency: float, codelet_id: str, parent_id: str,
    ):
        self.urgency = urgency
        self.codelet_id = codelet_id
        self.parent_id = parent_id

    @abstractmethod
    def run(self) -> Optional[Codelet]:
        pass
