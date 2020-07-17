from __future__ import annotations
from typing import Any, Callable, List, Optional, Union

from .hyper_parameters import HyperParameters


class Concept:

    DECAY_RATE = HyperParameters.DECAY_RATE
    MAXIMUM_DEPTH = HyperParameters.MAXIMUM_CONCEPT_DEPTH
    MAXIMUM_DISTANCE = HyperParameters.MAXIMUM_DISTANCE_FROM_PROTOTYPE

    def __init__(
        self,
        name: str,
        depth: int = 1,
        activation: float = 0.0,
        space: Optional[Concept] = None,
        prototype: Optional[Union[List[int], List[float], str]] = None,
        boundary: Optional[Union[List[int], List[float]]] = None,
        distance_metric: Optional[Callable] = None,
    ):
        if depth < 1:
            raise Exception(
                f"Creating concept {name} failed because "
                + f"depth {depth} is less than 1."
            )
        if boundary is not None and type(prototype) == str:
            raise Exception(
                f"Creating concept {name} failed because "
                + f"a concept with a symbolic prototype cannot have a boundary."
            )
        if boundary is not None and len(boundary) > 1:
            raise Exception(
                f"Creating concept {name} failed because "
                + f"boundary {boundary} is multidimensional."
            )
        if boundary is not None and len(boundary) != len(prototype):
            raise Exception(
                f"Creating concept {name} failed because "
                + f"prototype {prototype} and boundary {boundary} "
                + f"have different dimensionality."
            )
        if boundary == prototype and prototype is not None:
            raise Exception(
                f"Creating concept {name} failed because "
                + f" prototype and boundary are equal {prototype}."
            )
        self.name = name
        self.space = space
        self.depth = depth
        self.activation_coefficient = 1 / depth
        self.prototype = prototype
        self.boundary = boundary
        self.distance_metric = distance_metric
        self.activation = activation

    @property
    def depth_rating(self) -> float:
        return self._value_as_decimal(self.depth, self.MAXIMUM_DEPTH)

    def distance_from(self, candidate_instance: Any) -> float:
        """Return distance from prototype to candidate instance."""
        if self.distance_metric is None:
            raise Exception(f"Concept {self.name} has no distance metric.")
        raw_distance = self.distance_metric(self.prototype, candidate_instance)
        if self.boundary is not None and self.prototype[0] > self.boundary[0]:
            return 0 if candidate_instance[0] > self.prototype[0] else raw_distance
        if self.boundary is not None and self.prototype[0] < self.boundary[0]:
            return 0 if candidate_instance[0] < self.prototype[0] else raw_distance
        return raw_distance

    def distance_rating(self, candidate_instance: Any) -> float:
        distance = self.distance_from(candidate_instance)
        return self._value_as_decimal(distance, self.MAXIMUM_DISTANCE)

    def _value_as_decimal(self, value, maximum) -> float:
        return min(value / maximum, 1.0)

    def boost_activation(self, amount: float):
        raw_activation = self.activation + amount * self.activation_coefficient
        self.activation = 1.0 if raw_activation > 1.0 else raw_activation

    def decay_activation(self):
        raw_activation = self.activation - self.DECAY_RATE * self.activation_coefficient
        self.activation = 0.0 if raw_activation < 0.0 else raw_activation
