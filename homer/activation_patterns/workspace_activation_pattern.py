import math
import random
from typing import List, Tuple, Union

import numpy

from homer.activation_pattern import ActivationPattern
from homer.hyper_parameters import HyperParameters
from homer.workspace_location import WorkspaceLocation


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
        self.depth = depth
        self.height = height
        self.width = width
        self.activation_matrix = numpy.zeros([depth, height, width])
        self.activation_buffer = numpy.zeros([depth, height, width])
        self.depth_divisor = workspace_depth / depth
        self.height_divisor = workspace_height / height
        self.width_divisor = workspace_width / width

    def get_activation(self, location: List[Union[float, int]]) -> float:
        depth, height, width = self._depth_height_width(location)
        return self.activation_matrix[depth][height][width]

    def get_activation_at(self, location: WorkspaceLocation) -> float:
        return self.activation_matrix[location.i][location.j][location.k]

    def get_activation_as_scalar(self) -> float:
        return numpy.mean(self.activation_matrix)

    def get_high_location(self) -> WorkspaceLocation:
        i_s, j_s, k_s = (list(range(l)) for l in [self.depth, self.height, self.width])
        [random.shuffle(l) for l in [i_s, j_s, k_s]]
        for i in i_s:
            for j in j_s:
                for k in k_s:
                    if self.activation_matrix[i][j][k] == 1.0:
                        return WorkspaceLocation(i, j, k)
        raise ValueError("There is no highly activated cell in the activation pattern.")

    def get_spreading_signal(self) -> numpy.ndarray:
        return numpy.array(
            [
                [[0.1 if activation == 1 else 0 for activation in row] for row in layer]
                for layer in self.activation_matrix
            ]
        )

    def is_fully_activated(self) -> bool:
        return self.get_activation_as_scalar() >= 1.0

    def is_high(self) -> bool:
        return 1.0 in self.activation_matrix

    def boost_activation(self, amount: float, location: List[Union[float, int]]):
        depth, height, width = self._depth_height_width(location)
        current_activation = self.activation_matrix[depth][height][width]
        self.activation_buffer[depth][height][width] += (
            current_activation + amount * self.activation_coefficient
        )

    def boost_activation_evenly(self, amount: float):
        self.activation_buffer = numpy.add(
            self.activation_buffer, amount * self.activation_coefficient
        )

    def boost_activation_with_signal(self, signal: numpy.ndarray):
        self.activation_buffer = numpy.add(self.activation_buffer, signal)

    def decay_activation(self, location: List[Union[float, int]]):
        depth, height, width = self._depth_height_width(location)
        self.activation_buffer[depth][height][width] -= (
            self.DECAY_RATE * self.activation_coefficient
        )

    def update_activation(self):
        self.activation_matrix = numpy.add(
            self.activation_matrix, self.activation_buffer
        )
        self.activation_matrix = numpy.maximum(
            self.activation_matrix, numpy.zeros_like(self.activation_matrix)
        )
        self.activation_matrix = numpy.minimum(
            self.activation_matrix, numpy.ones_like(self.activation_matrix)
        )
        self.activation_matrix = numpy.array(
            [
                [
                    [
                        1.0 if activation > 0.5 and random.randint(0, 1) else activation
                        for activation in row
                    ]
                    for row in layer
                ]
                for layer in self.activation_matrix
            ]
        )
        self.activation_buffer = numpy.zeros_like(self.activation_buffer)

    def _depth_height_width(self, location: List[Union[float, int]]) -> Tuple[int]:
        depth = min(math.floor(location[0] / self.depth_divisor), self.depth - 1)
        height = min(math.floor(location[1] / self.height_divisor), self.height - 1)
        width = min(math.floor(location[2] / self.width_divisor), self.width - 1)
        return (depth, height, width)
