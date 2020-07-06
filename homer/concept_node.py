from __future__ import annotations
from typing import Any, Function


class ConceptNode:
    def __init__(
        self,
        name: str,
        space: ConceptNode,
        depth: float,
        prototype: Any,
        boundary: Any,
        distance_metric: Function,
        activation: float,
    ):
        self.name = name
        self.space = space
        self.depth = depth
        self.prototype = prototype
        self.boundary = boundary
        self.distance_metric = distance_metric
        self.activation = activation

    def distance_from(self, candidate_instance: Any) -> float:
        """Return distance from prototype to candidate instance."""
        raw_distance = self.distance_metric(self.prototype, candidate_instance)
        if self.boundary is None:
            return raw_distance
        if self.prototype > self.boundary:
            return 0 if candidate_instance > self.prototype else raw_distance
        if self.prototype < self.boundary:
            return 0 if candidate_instance < self.prototype else raw_distance
        else:
            raise Exception(
                f"Error calculating distance of {candidate_instance} "
                + f"from {self.name} with prototype {self.prototype} "
                + f"and boundary {self.boundary}."
            )
