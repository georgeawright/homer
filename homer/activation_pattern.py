import math
from abc import ABC, abstractmethod
from typing import List, Union

from homer.hyper_parameters import HyperParameters


class ActivationPattern(ABC):
    @abstractmethod
    def get_activation(self, location: List[Union[float, int]]) -> float:
        pass

    @abstractmethod
    def boost_activation(self, amount: float, location: List):
        pass

    @abstractmethod
    def decay_activation(self, location: List[Union[float, int]]):
        pass
