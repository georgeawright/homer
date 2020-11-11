from typing import Any, Callable, List

from homer.classifier import Classifier
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.hyper_parameters import HyperParameters
from homer.structure import Structure
from homer.structure_collection import StructureCollection

from .chunk import Chunk
from .link import Link
from .space import Space


class Concept(Structure):

    DISTANCE_TO_PROXIMITY_WEIGHT = HyperParameters.DISTANCE_TO_PROXIMITY_WEIGHT

    def __init__(
        self,
        name: str,
        prototype: Any,
        classifier: Classifier,
        parent_space: Space,
        relevant_value: str,
        child_spaces: StructureCollection,
        distance_function: Callable,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        depth: int = 1,
    ):
        location = None
        quality = None
        Structure.__init__(
            self, location, quality, links_in=links_in, links_out=links_out
        )
        self.name = name
        self.prototype = prototype
        self.classifier = classifier
        self.parent_space = parent_space
        self.relevant_value = relevant_value
        self.child_spaces = child_spaces
        self.distance_function = distance_function
        self.depth = depth

    def classify(self, example: Structure) -> FloatBetweenOneAndZero:
        return self.classifier.classify(self, example)

    def distance_from(self, other: Structure):
        return self.distance_function(
            self.prototype, getattr(other, self.relevant_value)
        )

    def proximity_to(self, other: Structure):
        return self._distance_to_proximity(self.distance_from(other))

    def distance_between(self, a: Structure, b: Structure):
        return self.distance_function(
            getattr(a, self.relevant_value), getattr(b, self.relevant_value)
        )

    def proximity_between(self, a: Structure, b: Structure):
        return self._distance_to_proximity(self.distance_between(a, b))

    def _distance_to_proximity(self, value: float) -> float:
        if value == 0:
            return 1.0
        inverse = 1.0 / value
        proximity = inverse * self.DISTANCE_TO_PROXIMITY_WEIGHT
        return min(proximity, 1.0)
