from __future__ import annotations


class HyperParameters:
    FLOATING_POINT_TOLERANCE = 1e-5
    CODELET_RUN_LIMIT = 20000

    ACTIVATION_UPDATE_FREQUENCY = 10
    ACTIVATION_UPDATE_COEFFICIENT = 0.5
    MINIMUM_ACTIVATION_UPDATE = 0.2
    DECAY_RATE = 0.02
    JUMP_THRESHOLD = 0.55

    MAXIMUM_CODERACK_POPULATION = 100
    MINIMUM_CODELET_URGENCY = 0.01
    NUMBER_OF_START_CHUNK_SUGGESTERS = 7

    MAXIMUM_DETERMINISM = 0.9
    MINIMUM_DETERMINISM = 0.3

    a = 0.9
    b = 0.0
    c = 0.00005
    d = 0.0

    # some alternative weights:
    # a = 0.7
    # b = 25.0
    # c = 0.0
    # d = 0.1

    DETERMINISM_SMOOTHING_FUNCTION = (
        lambda satisfaction, change_in_satisfaction, time_since_last_improvement: min(
            max(
                HyperParameters.a * satisfaction
                + HyperParameters.b * change_in_satisfaction
                - HyperParameters.c * time_since_last_improvement
                + HyperParameters.d,
                HyperParameters.MINIMUM_DETERMINISM,
            ),
            HyperParameters.MAXIMUM_DETERMINISM,
        )
    )

    # TODO: these ought to be specific to each conceptual space
    DISTANCE_TO_PROXIMITY_WEIGHT = 1
    HOW_FAR_IS_NEAR = 1

    ACTIVATION_LOGGING_FREQUENCY = 100

    TESTING = False

    RELATIVES_ACTIVATION_WEIGHT = 0.5
    INSTANCES_ACTIVATION_WEIGHT = 1.0

    VIEW_QUALITY_CORRESPONDENCE_WEIGHT = 0.5
    VIEW_QUALITY_INPUT_WEIGHT = 0.5

    RELATION_QUALITY_CLASSIFICATION_WEIGHT = 1.0
    RELATION_QUALITY_SAMENESS_WEIGHT = 0.0
    RELATION_QUALITY_TIME_WEIGHT = 0.0

    WORLDVIEW_QUALITY_CORRECTNESS_WEIGHT = 0.3
    WORLDVIEW_QUALITY_COMPLETENESS_WEIGHT = 0.2
    WORLDVIEW_QUALITY_CONCISENESS_WEIGHT = 0.0
    WORLDVIEW_QUALITY_COHESION_WEIGHT = 0.5

    BUBBLE_CHAMBER_SATISFACTION_MAIN_INPUT_WEIGHT = 0.4
    BUBBLE_CHAMBER_SATISFACTION_VIEW_QUALITIES_WEIGHT = 0.2
    BUBBLE_CHAMBER_SATISFACTION_WORLDVIEW_WEIGHT = 0.4
