from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet
from homer.id import ID


class Codelet(ABC):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        parent_concept: Optional[Concept],
        target_perceptlet: Perceptlet,
        urgency: float,
        parent_id: str,
    ):
        self.bubble_chamber = bubble_chamber
        self.perceptlet_type = perceptlet_type
        self.parent_concept = parent_concept
        self.target_perceptlet = target_perceptlet
        self.urgency = urgency
        self.codelet_id = ID.new(self)
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
