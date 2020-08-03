from typing import List, Union

from homer.activation_pattern import ActivationPattern


class ScalarActivationPattern(ActivationPattern):
    def __init__(self, activation_coefficient: float, activation: float = 0):
        self.activation_coefficient = activation_coefficient
        self.activation = activation

    def get_activation(self, location: List[Union[float, int]]):
        return self.activation

    def get_activation_as_scalar(self):
        return self.activation

    def boost_activation(self, amount: float, location: List[Union[float, int]]):
        raw_activation = self.activation + amount * self.activation_coefficient
        self.activation = 1.0 if raw_activation > 1.0 else raw_activation

    def boost_activation_evenly(self, amount: float):
        raw_activation = self.activation + amount * self.activation_coefficient
        self.activation = 1.0 if raw_activation > 1.0 else raw_activation

    def decay_activation(self, location: List[Union[float, int]]):
        raw_activation = self.activation - self.DECAY_RATE * self.activation_coefficient
        self.activation = 0.0 if raw_activation < 0.0 else raw_activation
