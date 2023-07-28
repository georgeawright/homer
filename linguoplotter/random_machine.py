import math
import random

from .errors import MissingStructureError
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters
from .tools import generalized_mean


class RandomMachine:
    FLOATING_POINT_TOLERANCE = HyperParameters.FLOATING_POINT_TOLERANCE
    SATISFACTION_WEIGHT = HyperParameters.DETERMINISM_WEIGHTS["satisfaction"]
    CHANGE_IN_SATISFACTION_WEIGHT = HyperParameters.DETERMINISM_WEIGHTS[
        "change_in_satisfaction"
    ]
    TIME_SINCE_IMPROVEMENT_WEIGHT = HyperParameters.DETERMINISM_WEIGHTS[
        "time_since_last_improvement"
    ]
    BIAS_WEIGHT = HyperParameters.DETERMINISM_WEIGHTS["bias"]
    MINIMUM_DETERMINISM = HyperParameters.MINIMUM_DETERMINISM
    MAXIMUM_DETERMINISM = HyperParameters.MAXIMUM_DETERMINISM

    def __init__(self, bubble_chamber: "BubbleChamber", seed: int = None):
        self.bubble_chamber = bubble_chamber
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self.codelets_run = 0
        self.determinism = 0
        self.randomness = 1

    def recalculate_determinism(self) -> FloatBetweenOneAndZero:
        codelets_since_successful_focus_unset = (
            self.codelets_run - self.bubble_chamber.time_of_last_successful_focus_unset
        )
        self.determinism = (
            self.BIAS_WEIGHT
            + self.bubble_chamber.satisfaction * self.SATISFACTION_WEIGHT
            + self.bubble_chamber.change_in_satisfaction
            * self.CHANGE_IN_SATISFACTION_WEIGHT
            - codelets_since_successful_focus_unset * self.TIME_SINCE_IMPROVEMENT_WEIGHT
        )
        if self.determinism < self.MINIMUM_DETERMINISM:
            self.determinism = self.MINIMUM_DETERMINISM
        elif self.determinism > self.MAXIMUM_DETERMINISM:
            self.determinism = self.MAXIMUM_DETERMINISM
        self.randomness = 1 - self.determinism

    def generate_number(self, minimum: float = 0.0) -> FloatBetweenOneAndZero:
        if minimum > 1:
            raise Exception("Minimum should be lower than 1")
        if minimum == 0.0:
            return random.random()
        return (minimum / 1) * random.random() + minimum

    def coin_flip(self) -> bool:
        return self.generate_number() > 0.5

    def randomize_number(self, number: FloatBetweenOneAndZero):
        return number * self.determinism + random.random() * self.randomness

    def select(
        self,
        collection: dict,
        key: callable = lambda x: 0,
        exclude: list = None,
        verbose: bool = False,
    ):
        exclude = [] if exclude is None else exclude
        for element in exclude:
            if element in collection:
                collection.pop(element)
        if len(collection) < 1:
            raise MissingStructureError
        if len(collection) == 1:
            for item in collection:
                return item
        sample_size = min(
            math.ceil(len(collection) * self.determinism) + 1,
            len(collection),
        )
        sample = random.sample(list(collection), sample_size)
        key_weights = [key(item) for item in sample]
        random_weights = [self.generate_number() for item in sample]
        highest_weight = 0
        index_of_highest_weight = 0
        for i in range(len(sample)):
            weight = (
                key_weights[i] * self.determinism + random_weights[i] * self.randomness
            )
            if verbose:
                print(sample[i], weight)
            if weight > highest_weight:
                highest_weight = weight
                index_of_highest_weight = i

        return sample[index_of_highest_weight]
