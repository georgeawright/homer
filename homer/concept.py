from __future__ import annotations
from typing import Any, Callable, List, Optional, Union


class Concept:
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
        self.prototype = prototype
        self.boundary = boundary
        self.distance_metric = distance_metric
        self.activation = activation

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
