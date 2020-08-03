from homer.activation_patterns.scalar_activation_pattern import ScalarActivationPattern
from homer.concept import Concept


class PerceptletType(Concept):
    def __init__(self, name: str, depth: int = 1):
        activation_coefficient = 1 / depth
        activation_pattern = ScalarActivationPattern(activation_coefficient)
        Concept.__init__(
            self, name, activation_pattern, depth=depth,
        )
