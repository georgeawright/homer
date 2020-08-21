from __future__ import annotations
from typing import List, Union

from homer.activation_pattern import ActivationPattern
from homer.workspace_location import WorkspaceLocation


class ScalarActivationPattern(ActivationPattern):
    def __init__(self, activation_coefficient: float, activation: float = 0):
        self.activation_coefficient = activation_coefficient
        self.activation = activation
        self.activation_buffer = 0

    def __eq__(self, other: ActivationPattern) -> bool:
        return self.as_scalar() == other.as_scalar()

    def __gt__(self, other: ActivationPattern) -> bool:
        return self.as_scalar() > other.as_scalar()

    def __lt__(self, other: ActivationPattern) -> bool:
        return self.as_scalar() < other.as_scalar()

    def at(self, location: WorkspaceLocation) -> float:
        return self.activation

    def as_scalar(self) -> float:
        return self.activation

    def get_spreading_signal(self) -> float:
        return 0.1 * self.is_full()

    def is_full(self) -> bool:
        return self.activation >= 1.0

    def is_high(self) -> bool:
        return self.activation >= 1.0

    def boost(self, amount: float, location: WorkspaceLocation):
        self.activation_buffer += self.activation + amount * self.activation_coefficient

    def boost_evenly(self, amount: float):
        self.boost(amount, None)

    def boost_with_signal(self, signal: float):
        self.boost(signal, None)

    def decay(self, location: WorkspaceLocation):
        self.activation_buffer -= (
            self.activation - self.DECAY_RATE * self.activation_coefficient
        )

    def update(self):
        self.activation = min(max(self.activation + self.activation_buffer, 0.0), 1.0)
        self.activation_buffer = 0.0
