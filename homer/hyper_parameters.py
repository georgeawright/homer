class HyperParameters:
    FLOATING_POINT_TOLERANCE = 1e-5

    ACTIVATION_UPDATE_FREQUENCY = 10
    ACTIVATION_UPDATE_COEFFICIENT = 0.5
    MINIMUM_ACTIVATION_UPDATE = 0.01
    DECAY_RATE = 0.01

    MAXIMUM_CODERACK_POPULATION = 100
    MINIMUM_CODELET_URGENCY = 0.01

    DETERMINISM_SMOOTHING_FUNCTION = lambda x: (x + 0.5) / 2

    # TODO: these ought to be removed when suggesters are implemented
    CONFIDENCE_THRESHOLD = 0.5

    # TODO: these ought to be specific to each conceptual space
    DISTANCE_TO_PROXIMITY_WEIGHT = 1.5
    HOW_FAR_IS_NEAR = 1.5
