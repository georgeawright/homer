from typing import List, Union

from homer.activation_pattern import ActivationPattern


class ScalarActivationPattern(ActivationPattern):
    def __init__(self, activation_coefficient: float, activation: float = 0):
        self.activation_coefficient = activation_coefficient
        self.activation = activation
        self.activation_buffer = 0

    def get_activation(self, location: List[Union[float, int]]):
        return self.activation

    def get_activation_as_scalar(self):
        return self.activation

    def boost_activation(self, amount: float, location: List[Union[float, int]]):
        self.activation_buffer += self.activation + amount * self.activation_coefficient
        print(self.activation_buffer)

    def boost_activation_evenly(self, amount: float):
        self.activation_buffer += self.activation + amount * self.activation_coefficient

    def decay_activation(self, location: List[Union[float, int]]):
        self.activation_buffer -= (
            self.activation - self.DECAY_RATE * self.activation_coefficient
        )

    def update_activation(self):
        self.activation = min(max(self.activation + self.activation_buffer, 0.0), 1.0)
        self.activation_buffer = 0.0
