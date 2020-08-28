from __future__ import annotations
from typing import Any, Callable, List, Optional, Set, Union

from homer.activation_pattern import ActivationPattern
from homer.bubble import Bubble
from homer.workspace_location import WorkspaceLocation


class Concept(Bubble):
    def __init__(
        self,
        name: str,
        activation: ActivationPattern,
        depth: int = 1,
        space: Optional[Concept] = None,
        prototype: Optional[Union[List[int], List[float], str]] = None,
        boundary: Optional[Union[List[int], List[float]]] = None,
        relevant_value: Optional[str] = None,
        distance_metric: Optional[Callable] = None,
        connections: Optional[Set[Concept]] = None,
    ):
        if depth < 1:
            raise Exception(
                f"Creating concept {name} failed because "
                + f"depth {depth} is less than 1."
            )
        if boundary is not None and type(prototype) == str:
            raise Exception(
                f"Creating concept {name} failed because "
                + "a concept with a symbolic prototype cannot have a boundary."
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
                + "have different dimensionality."
            )
        if boundary == prototype and prototype is not None:
            raise Exception(
                f"Creating concept {name} failed because "
                + f" prototype and boundary are equal {prototype}."
            )
        self.concept_id = "concept_" + name.upper()
        Bubble.__init__(self, activation, self.concept_id)
        self.name = name
        self.space = space
        self.depth = depth
        self.activation_coefficient = 1 / depth
        self.prototype = prototype
        self.boundary = boundary
        self.relevant_value = "value" if relevant_value is None else relevant_value
        self.distance_metric = distance_metric
        self.connections = set() if connections is None else connections

    @property
    def depth_rating(self) -> float:
        return 1 / self.depth

    def spawn_codelet(self):
        raise NotImplementedError

    def spread_activation(self) -> None:
        signal = self.activation.get_spreading_signal()
        for connection in self.connections:
            connection.activation.boost_with_signal(signal)

    def distance_from(self, candidate_instance: Any) -> float:
        """Return distance from prototype to candidate instance."""
        raw_distance = self.distance_between(self.prototype, candidate_instance)
        if self.boundary is not None and self.prototype[0] > self.boundary[0]:
            return 0 if candidate_instance[0] > self.prototype[0] else raw_distance
        if self.boundary is not None and self.prototype[0] < self.boundary[0]:
            return 0 if candidate_instance[0] < self.prototype[0] else raw_distance
        return raw_distance

    def distance_between(self, a: Any, b: Any) -> float:
        if self.distance_metric is None:
            raise Exception(f"Concept {self.name} has no distance metric.")
        return self.distance_metric(a, b)

    def proximity_to(self, candidate_instance: Any) -> float:
        """returns a score of proximity: 0 is far, 1 is close"""
        distance = self.distance_from(candidate_instance)
        return self._distance_to_proximity(distance)

    def proximity_between(self, a: Any, b: Any) -> float:
        """returns a score of proximity: 0 is far, 1 is close"""
        distance = self.distance_between(a, b)
        return self._distance_to_proximity(distance)

    def _distance_to_proximity(self, value) -> float:
        if value == 0:
            return 1.0
        inverse = 1.0 / value
        proximity = inverse * self.DISTANCE_TO_PROXIMITY_WEIGHT
        return min(proximity, 1.0)

    @staticmethod
    def most_active(
        a: Concept, b: Concept, location: Optional[WorkspaceLocation] = None
    ):
        if location is None:
            return a if a.activation.as_scalar() > b.activation.as_scalar() else b
        return a if a.activation.at(location) > b.activation.at(location) else b
