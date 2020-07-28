import math
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
        self.depth_divisor = workspace_depth / depth
        self.height_divisor = workspace_height / height
        self.width_divisor = workspace_width / width

    def boost_activation(self, amount: float, location: List[Union[float, int]]):
        depth, height, width = self._depth_height_width(location)
        current_activation = self.activation_matrix[depth][height][width]
        raw_activation = current_activation + amount * self.activation_coefficient
        new_activation = 1.0 if raw_activation > 1.0 else raw_activation
        self.activation_matrix[depth][height][width] = new_activation

    def decay_activation(self, location: List[Union[float, int]]):
        depth, height, width = self._depth_height_width(location)
        current_activation = self.activation_matrix[depth][height][width]
        raw_activation = (
            current_activation - self.DECAY_RATE * self.activation_coefficient
        )
        new_activation = 0.0 if raw_activation < 0.0 else raw_activation
        self.activation_matrix[depth][height][width] = new_activation

    def _depth_height_width(self, location: List[Union[float, int]]) -> Tuple[int]:
        depth = math.floor(location[0] / self.depth_divisor)
        height = math.floor(location[1] / self.height_divisor)
        width = math.floor(location[2] / self.width_divisor)
        return (depth, height, width)
