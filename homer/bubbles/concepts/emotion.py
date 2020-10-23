from typing import Optional

from homer.activation_patterns import WorkspaceActivationPattern
from homer.bubbles.concept import Concept
from homer.hyper_parameters import HyperParameters


class Emotion(Concept):

    EMOTION_CONCEPTUAL_DEPTH = HyperParameters.EMOTION_CONCEPTUAL_DEPTH

    def __init__(self, name: str, depth: Optional[int] = None):
        depth = depth if depth is not None else self.EMOTION_CONCEPTUAL_DEPTH
        activation_coefficient = 1 / depth
        activation_pattern = WorkspaceActivationPattern(activation_coefficient)
        Concept.__init__(
            self,
            name,
            activation_pattern,
            depth=depth,
        )
