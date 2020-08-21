from typing import Optional

from .scalar_activation_pattern import ScalarActivationPattern


class PerceptletActivationPattern(ScalarActivationPattern):
    def __init__(self, activation: Optional[float] = None):
        self.activation = activation if activation is not None else 0.0
