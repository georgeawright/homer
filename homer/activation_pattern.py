from abc import ABC, abstractmethod
from typing import List, Union

from .hyper_parameters import HyperParameters
from .workspace_location import WorkspaceLocation


class ActivationPattern(ABC):

    DECAY_RATE = HyperParameters.DECAY_RATE

    @abstractmethod
    def at(self, location: WorkspaceLocation) -> float:
        pass

    @abstractmethod
    def as_scalar(self) -> float:
        pass

    @abstractmethod
    def get_spreading_signal(self) -> Union[float, list]:
        pass

    @abstractmethod
    def is_full(self) -> bool:
        pass

    @abstractmethod
    def is_high(self) -> bool:
        pass

    @abstractmethod
    def boost(self, amount: float, location: WorkspaceLocation):
        pass

    @abstractmethod
    def boost_evenly(self, amount: float):
        pass

    @abstractmethod
    def boost_with_signal(self, signal: Union[float, list]):
        pass

    @abstractmethod
    def decay(self, location: WorkspaceLocation):
        pass

    @abstractmethod
    def update(self):
        pass
