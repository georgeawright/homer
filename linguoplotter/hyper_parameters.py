from __future__ import annotations
from dataclasses import dataclass
import math

from .tools import generalized_mean


@dataclass
class HyperParameters:
    TESTING: bool = False

    CODELET_RUN_LIMIT: int = 20000
    ACTIVATION_LOGGING_FREQUENCY: int = 100

    FLOATING_POINT_TOLERANCE: float = 1e-5

    MAXIMUM_CODERACK_POPULATION: int = 100
    MINIMUM_CODELET_URGENCY: float = 0.01
    NUMBER_OF_START_CHUNK_SUGGESTERS: int = 7

    DEFAULT_DISTANCE_TO_PROXIMITY_WEIGHT: int = 1

    ACTIVATION_UPDATE_FREQUENCY: int = 10
    ACTIVATION_UPDATE_COEFFICIENT: float = 0.5
    MINIMUM_ACTIVATION_UPDATE: float = 0.2
    DECAY_RATE: float = 0.02
    JUMP_THRESHOLD: float = 0.55
    ACTIVATION_UPDATE_RELATIVES_WEIGHT: float = 0.5
    ACTIVATION_UPDATE_INSTANCES_WEIGHT: float = 1.0

    RANDOMNESS_IN_CORRESPONDENCE_START_SEARCH: float = 1.0

    MINIMUM_DETERMINISM: float = 0.3
    MAXIMUM_DETERMINISM: float = 0.9
    DETERMINISM_SATISFACTION_WEIGHT: float = 1.0
    DETERMINISM_CHANGE_IN_SATISFACTION_WEIGHT: float = 0.0
    DETERMINISM_TIME_SINCE_IMPROVEMENT_WEIGHT: float = 0.00005
    DETERMINISM_BIAS_WEIGHT: float = 0.0

    # exponents determine the type of mean
    # inf = max, 1 = arithmetic, 0 = geometric, -1 = harmonic, -inf = min

    BUBBLE_CHAMBER_SATISFACTION_MAIN_INPUT_WEIGHT: float = 0.4
    BUBBLE_CHAMBER_SATISFACTION_VIEWS_WEIGHT: float = 0.2
    BUBBLE_CHAMBER_SATISFACTION_WORLDVIEW_WEIGHT: float = 0.4
    BUBBLE_CHAMBER_SATISFACTION_EXPONENT: float = 1.0

    # Accuracy:
    # quality of relations between input and text
    WORLDVIEW_QUALITY_CORRECTNESS_WEIGHT: float = 0.25
    # relative size of input
    WORLDVIEW_QUALITY_COMPLETENESS_WEIGHT: float = 0.25
    # Quality:
    # quality of relations within text
    WORLDVIEW_QUALITY_COHESIVENESS_WEIGHT: float = 0.25
    # relative size of output
    WORLDVIEW_QUALITY_CONCISENESS_WEIGHT: float = 0.25
    WORLDVIEW_QUALITY_EXPONENT: float = -1.0

    VIEW_QUALITY_CORRESPONDENCE_WEIGHT: float = 0.5
    VIEW_QUALITY_INPUT_WEIGHT: float = 0.5
    VIEW_QUALITY_EXPONENT: float = -math.inf
    VIEW_QUALITY_INPUT_EXPONENT: float = 1.0

    RELATION_QUALITY_CLASSIFICATION_WEIGHT: float = 1.0
    RELATION_QUALITY_SAMENESS_WEIGHT: float = 0.0
    RELATION_QUALITY_TIME_WEIGHT: float = 0.0
    RELATION_QUALITY_EXPONENT: float = 1.0

    @classmethod
    def from_dict(cls, dictionary):
        return cls(**dictionary)
