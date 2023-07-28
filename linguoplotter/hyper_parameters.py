from __future__ import annotations
import math

from .tools import generalized_mean


class HyperParameters:
    """Default hyper-parameters. These should be altered before loading a program in the interpreter"""

    TESTING = False

    CODELET_RUN_LIMIT = 20000
    ACTIVATION_LOGGING_FREQUENCY = 100

    FLOATING_POINT_TOLERANCE = 1e-5

    MAXIMUM_CODERACK_POPULATION = 100
    MINIMUM_CODELET_URGENCY = 0.01
    NUMBER_OF_START_CHUNK_SUGGESTERS = 7

    DEFAULT_DISTANCE_TO_PROXIMITY_WEIGHT = 1

    ACTIVATION_UPDATE_FREQUENCY = 10
    ACTIVATION_UPDATE_COEFFICIENT = 0.5
    MINIMUM_ACTIVATION_UPDATE = 0.2
    DECAY_RATE = 0.02
    JUMP_THRESHOLD = 0.55
    ACTIVATION_UPDATE_WEIGHTS = {
        "relatives": 0.5,
        "instances": 1.0,
    }

    MINIMUM_DETERMINISM = 0.3
    MAXIMUM_DETERMINISM = 0.9
    DETERMINISM_WEIGHTS = {
        "satisfaction": 1.0,
        "change_in_satisfaction": 0.0,
        "time_since_last_improvement": 0.00005,
        "bias": 0.0,
    }

    # exponents determine the type of mean
    # inf = max, 1 = arithmetic, 0 = geometric, -1 = harmonic, -inf = min

    BUBBLE_CHAMBER_SATISFACTION_WEIGHTS = {
        "main_input": 0.4,
        "views": 0.2,
        "worldview": 0.4,
    }
    BUBBLE_CHAMBER_SATISFACTION_EXPONENT = 1

    WORLDVIEW_QUALITY_WEIGHTS = {
        # Accuracy:
        "correctness": 0.25,  # quality of relations between input and text
        "completeness": 0.25,  # relative size of input
        # Quality:
        "cohesiveness": 0.25,  # quality of relations within text
        "conciseness": 0.25,  # relative size of output
    }
    WORLDVIEW_QUALITY_EXPONENT = -1

    VIEW_QUALITY_WEIGHTS = {
        "correspondences": 0.5,
        "input": 0.5,
    }
    VIEW_QUALITY_EXPONENT = -math.inf

    RELATION_QUALITY_WEIGHTS = {
        "classification": 1.0,
        "sameness": 0.0,
        "time": 0.0,
    }
    RELATION_QUALITY_EXPONENT = 1
