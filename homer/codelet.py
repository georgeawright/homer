from __future__ import annotations
import uuid
from abc import ABC, abstractmethod
from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.hyper_parameters import HyperParameters


class Codelet(ABC):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(self, bubble_chamber: BubbleChamber, parent_id: str):
        self.bubble_chamber = bubble_chamber
        self.codelet_id = "codelet_" + uuid.uuid4().hex
        self.parent_id = parent_id

    def run(self) -> Optional[Codelet]:
        if self._passes_preliminary_checks():
            self._calculate_confidence()
            if self.confidence > self.CONFIDENCE_THRESHOLD:
                self._boost_activations()
                self._process_perceptlet()
                return self._engender_follow_up()
        return self._fizzle()

    def _boost_activations(self):
        if self.parent_concept is not None:
            self.parent_concept.boost_activation(
                self.confidence, self.target_perceptlet.location
            )
        self.perceptlet_type.boost_activation(
            self.confidence, self.target_perceptlet.location
        )

    @abstractmethod
    def _passes_preliminary_checks(self) -> bool:
        pass

    @abstractmethod
    def _fizzle(self) -> Optional[Codelet]:
        pass

    @abstractmethod
    def _calculate_confidence(self):
        pass

    @abstractmethod
    def _process_perceptlet(self):
        pass

    @abstractmethod
    def _engender_follow_up(self) -> Codelet:
        pass
