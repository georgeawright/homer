import numpy
import random

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

    def at(self, location: WorkspaceLocation) -> float:
        return self.activation_matrix[location.i][location.j][location.k]

    def as_scalar(self) -> float:
        return numpy.mean(self.activation_matrix)

    def get_high_location(self) -> WorkspaceLocation:
        i_s, j_s, k_s = (list(range(x)) for x in [self.depth, self.height, self.width])
        [random.shuffle(coordinates) for coordinates in [i_s, j_s, k_s]]
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

    def is_full(self) -> bool:
        return self.as_scalar() >= 1.0

    def is_high(self) -> bool:
        return 1.0 in self.activation_matrix

    def boost(self, amount: float, location: WorkspaceLocation):
        self.activation_buffer[location.i][location.j][location.k] += (
            amount * self.activation_coefficient
        )

    def boost_evenly(self, amount: float):
        self.activation_buffer = numpy.add(
            self.activation_buffer, amount * self.activation_coefficient
        )

    def boost_with_signal(self, signal: numpy.ndarray):
        self.activation_buffer = numpy.add(self.activation_buffer, signal)

    def decay(self, location: WorkspaceLocation):
        self.activation_buffer[location.i][location.j][location.k] -= (
            self.DECAY_RATE * self.activation_coefficient
        )

    def update(self):
        if numpy.array_equal(
            self.activation_buffer, numpy.zeros_like(self.activation_buffer)
        ):
            self.boost_evenly(-self.DECAY_RATE)
        for i, layer in enumerate(self.activation_matrix):
            for j, row in enumerate(layer):
                for k, cell in enumerate(row):
                    raw_new_activation = cell + self.activation_buffer[i][j][k]
                    if (
                        raw_new_activation > 0.5
                        and random.randint(0, 1)
                        and self.activation_buffer[i][j][k] > 0
                    ):
                        self.activation_matrix[i][j][k] = 1.0
                    elif raw_new_activation > 1.0:
                        self.activation_matrix[i][j][k] = 1.0
                    elif raw_new_activation < 0.0:
                        self.activation_matrix[i][j][k] = 0.0
                    else:
                        self.activation_matrix[i][j][k] = raw_new_activation
        self.activation_buffer = numpy.zeros_like(self.activation_buffer)
