import math
import random
from typing import Union

from .errors import MissingStructureError
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters


class RandomMachine:
    def __init__(self, bubble_chamber: "BubbleChamber", seed: int = None):
        self.bubble_chamber = bubble_chamber
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self.determinism_smoothing_function = (
            HyperParameters.DETERMINISM_SMOOTHING_FUNCTION
        )

    @property
    def determinism(self) -> FloatBetweenOneAndZero:
        return self.determinism_smoothing_function(self.bubble_chamber.satisfaction)

    @property
    def randomness(self) -> FloatBetweenOneAndZero:
        return 1 - self.determinism

    def generate_number(self) -> FloatBetweenOneAndZero:
        return random.random()

    def randomize_number(self, number: FloatBetweenOneAndZero):
        return number * self.determinism + random.random() * self.randomness

    def select(
        self,
        collection: dict,
        key: callable = lambda x: 0,
        exclude: list = None,
    ):
        exclude = [] if exclude is None else exclude
        for element in exclude:
            if element in collection:
                collection.pop(element)
        if len(collection) < 1:
            raise MissingStructureError
        sample_size = max(math.ceil(len(collection) * self.determinism), 1)
        sample = random.sample(list(collection), sample_size)
        key_weights = [key(item) for item in sample]
        random_weights = [random.random() for item in sample]
        total_key_weights = sum(key_weights)
        total_random_weight = sum(random_weights)
        if total_key_weights > 0:
            key_weights = [w / total_key_weights for w in key_weights]
        if total_random_weight > 0:
            random_weights = [w / total_random_weight for w in random_weights]

        highest_weight = 0
        index_of_highest_weight = 0
        for i in range(len(sample)):
            weight = (
                key_weights[i] * self.determinism + random_weights[i] * self.randomness
            )
            if weight > highest_weight:
                highest_weight = weight
                index_of_highest_weight = i

        return sample[index_of_highest_weight]
