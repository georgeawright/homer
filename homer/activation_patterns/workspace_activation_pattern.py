import math
import statistics
from typing import List, Tuple, Union

from homer.hyper_parameters import HyperParameters
from homer.activation_pattern import ActivationPattern


class WorkspaceActivationPattern(ActivationPattern):
    def __init__(
        self,
        activation_coefficient,
        depth: int = HyperParameters.ACTIVATION_PATTERN_DEPTH,
        height: int = HyperParameters.ACTIVATION_PATTERN_HEIGHT,
        width: int = HyperParameters.ACTIVATION_PATTERN_WIDTH,
        workspace_depth: int = HyperParameters.WORKSPACE_DEPTH,
        workspace_height: int = HyperParameters.WORKSPACE_HEIGHT,
        workspace_width: int = HyperParameters.WORKSPACE_WIDTH,
    ):
        self.activation_coefficient = activation_coefficient
        self.activation_matrix = [
            [[0.0 for _ in range(width)] for _ in range(height)] for _ in range(depth)
        ]
        self.activation_buffer = [
            [[0.0 for _ in range(width)] for _ in range(height)] for _ in range(depth)
        ]
        self.depth_divisor = workspace_depth / depth
        self.height_divisor = workspace_height / height
        self.width_divisor = workspace_width / width

    def get_activation(self, location: List[Union[float, int]]) -> float:
        depth, height, width = self._depth_height_width(location)
        return self.activation_matrix[depth][height][width]

    def get_activation_as_scalar(self) -> float:
        return statistics.fmean(
            (
                activation
                for layer in self.activation_matrix
                for row in layer
                for activation in row
            )
        )

    def is_fully_activated(self) -> bool:
        return self.get_activation_as_scalar() >= 1.0

    def boost_activation(self, amount: float, location: List[Union[float, int]]):
        depth, height, width = self._depth_height_width(location)
        current_activation = self.activation_matrix[depth][height][width]
        self.activation_buffer[depth][height][width] += (
            current_activation + amount * self.activation_coefficient
        )

    def boost_activation_evenly(self, amount: float):
        for i, layer in enumerate(self.activation_buffer):
            for j, row in enumerate(layer):
                for k, _ in enumerate(row):
                    self.activation_buffer[i][j][k] += (
                        amount * self.activation_coefficient
                    )

    def decay_activation(self, location: List[Union[float, int]]):
        depth, height, width = self._depth_height_width(location)
        self.activation_buffer[depth][height][width] -= (
            self.DECAY_RATE * self.activation_coefficient
        )

    def _depth_height_width(self, location: List[Union[float, int]]) -> Tuple[int]:
        depth = math.floor(location[0] / self.depth_divisor)
        height = math.floor(location[1] / self.height_divisor)
        width = math.floor(location[2] / self.width_divisor)
        return (depth, height, width)

    def update_activation(self):
        for i, layer in enumerate(self.activation_matrix):
            for j, row in enumerate(layer):
                for k, cell in enumerate(row):
                    self.activation_matrix[i][j][k] = min(
                        max(cell + self.activation_buffer[i][j][k], 0.0), 1.0
                    )
                    self.activation_buffer[i][j][k] = 0.0
