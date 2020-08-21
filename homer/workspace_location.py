from __future__ import annotations
import math
from typing import List, Union

from .hyper_parameters import HyperParameters


class WorkspaceLocation:

    DEPTH = HyperParameters.ACTIVATION_PATTERN_DEPTH
    HEIGHT = HyperParameters.ACTIVATION_PATTERN_HEIGHT
    WIDTH = HyperParameters.ACTIVATION_PATTERN_WIDTH
    WORKSPACE_DEPTH = HyperParameters.WORKSPACE_DEPTH
    WORKSPACE_HEIGHT = HyperParameters.WORKSPACE_HEIGHT
    WORKSPACE_WIDTH = HyperParameters.WORKSPACE_WIDTH
    DEPTH_DIVISOR = WORKSPACE_DEPTH / DEPTH
    HEIGHT_DIVISOR = WORKSPACE_HEIGHT / HEIGHT
    WIDTH_DIVISOR = WORKSPACE_WIDTH / WIDTH

    def __init__(self, i: int, j: int, k: int):
        self.i = i
        self.j = j
        self.k = k

    @classmethod
    def from_workspace_coordinates(
        cls, coordinates: List[Union[float, int]]
    ) -> WorkspaceLocation:
        i = min(math.floor(coordinates[0] / cls.DEPTH_DIVISOR), cls.DEPTH - 1)
        j = min(math.floor(coordinates[1] / cls.HEIGHT_DIVISOR), cls.HEIGHT - 1)
        k = min(math.floor(coordinates[2] / cls.WIDTH_DIVISOR), cls.WIDTH - 1)
        return cls(i, j, k)
