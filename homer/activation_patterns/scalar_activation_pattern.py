from typing import List, Union

from homer.activation_pattern import ActivationPattern


class ScalarActivationPattern(ActivationPattern):
    def __init__(self, activation_coefficient: float, activation: float = 0):
        self.activation_coefficient = activation_coefficient
        self.activation = activation
        self.activation_buffer = 0

    def get_activation(self, location: List[Union[float, int]]) -> float:
        return self.activation

    def get_activation_as_scalar(self) -> float:
        return self.activation

    def get_spreading_signal(self) -> float:
        return 0.1 * self.is_fully_activated()

    def is_fully_activated(self) -> bool:
        return self.activation >= 1.0

    def is_high(self) -> bool:
        return self.activation >= 1.0

    def boost_activation(self, amount: float, location: List[Union[float, int]]):
        self.activation_buffer += self.activation + amount * self.activation_coefficient

    def boost_activation_evenly(self, amount: float):
        self.boost_activation(amount, [])

    def boost_activation_with_signal(self, signal: float):
        self.boost_activation(signal, [])

    def decay_activation(self, location: List[Union[float, int]]):
        self.activation_buffer -= (
            self.activation - self.DECAY_RATE * self.activation_coefficient
        )

    def update_activation(self):
        self.activation = min(max(self.activation + self.activation_buffer, 0.0), 1.0)
        self.activation_buffer = 0.0
