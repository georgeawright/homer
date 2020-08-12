import math
from abc import ABC, abstractmethod
from typing import Any, List, Union

from homer.hyper_parameters import HyperParameters


class ActivationPattern(ABC):

    DECAY_RATE = HyperParameters.DECAY_RATE

    @abstractmethod
    def get_activation(self, location: List[Union[float, int]]) -> float:
        pass

    @abstractmethod
    def get_activation_as_scalar(self) -> float:
        pass

    @abstractmethod
    def get_spreading_signal(self) -> Union[float, list]:
        pass

    @abstractmethod
    def is_fully_activated(self) -> bool:
        pass

    @abstractmethod
    def is_high(self) -> bool:
        pass

    @abstractmethod
    def boost_activation(self, amount: float, location: List):
        pass

    @abstractmethod
    def boost_activation_evenly(self, amount: float):
        pass

    @abstractmethod
    def boost_activation_with_signal(self, signal: Union[float, list]):
        pass

    @abstractmethod
    def decay_activation(self, location: List[Union[float, int]]):
        pass

    @abstractmethod
    def update_activation(self):
        pass
