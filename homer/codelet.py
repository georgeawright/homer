from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from .bubble_chamber import BubbleChamber
from .bubbles.concept import Concept
from .bubbles.concepts.perceptlet_type import PerceptletType
from .bubbles.perceptlet import Perceptlet
from .hyper_parameters import HyperParameters
from .id import ID
from .workspace_location import WorkspaceLocation


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
        self.location = WorkspaceLocation.from_workspace_coordinates(
            self.target_perceptlet.location
        )
        self.codelet_id = ID.new(self)
        self.parent_id = parent_id

    def run(self) -> Optional[Codelet]:
        if not self._passes_preliminary_checks():
            return self._fizzle()
        self._calculate_confidence()
        if self.confidence > self.CONFIDENCE_THRESHOLD:
            self._boost_activations()
            self._process_perceptlet()
            return self._engender_follow_up()
        return self._fail()

    def _boost_activations(self):
        if self.parent_concept is not None:
            self.parent_concept.activation.boost(self.confidence, self.location)
        self.perceptlet_type.activation.boost(self.confidence, self.location)

    def _decay_concept(self, concept: Concept):
        concept.activation.decay(self.location)

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

    @abstractmethod
    def _fail(self) -> Optional[Codelet]:
        pass
