import math
from abc import ABC, abstractmethod
from typing import List

from homer.hyper_parameters import HyperParameters


class ActivationPattern(ABC):
    @abstractmethod
    def boost_activation(self, amount: float, location: List):
        pass
        depth = math.floor(location[0] / self.WORKSPACE_DEPTH)
        height = math.floor(location[1] / self.WORKSPACE_HEIGHT)
        width = math.floor(location[2] / self.WORKSPACE_WIDTH)
        current_activation = self.activation_matrix[depth][height][width]
        raw_activation = current_activation + amount * self.activation_coefficient
        new_activation = 1.0 if raw_activation > 1.0 else raw_activation
        self.activation_matrix[depth][height][width] = new_activation
