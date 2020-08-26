from typing import Optional

from homer.hyper_parameters import HyperParameters

from .scalar_activation_pattern import ScalarActivationPattern


class PerceptletActivationPattern(ScalarActivationPattern):
    def __init__(self, activation: Optional[float] = None):
        activation_coefficient = HyperParameters.PERCEPTLET_ACTIVATION_COEFFICIENT
        activation = activation if activation is not None else 0.0
        ScalarActivationPattern.__init__(self, activation_coefficient, activation)

    def boost_by_amount(self, amount: float):
        raw_activation = self.activation + amount * self.activation_coefficient
        self.activation = min(max(raw_activation, 0.0), 1.0)

    def decay_by_amount(self, amount: float):
        self.boost_by_amount(-amount)
