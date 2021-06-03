from __future__ import annotations
from typing import Callable, List

from homer.classifier import Classifier
from homer.hyper_parameters import HyperParameters
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Node, Space


class Concept(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        locations: List[Location],
        classifier: Classifier,
        instance_type: type,
        parent_space: Space,
        child_spaces: StructureCollection,
        distance_function: Callable,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        depth: int = 1,
        distance_to_proximity_weight: float = HyperParameters.DISTANCE_TO_PROXIMITY_WEIGHT,
    ):
        quality = None
        Node.__init__(
            self,
            structure_id,
            parent_id,
            locations=locations,
            parent_space=parent_space,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.name = name
        self.classifier = classifier
        self.instance_type = instance_type
        self.child_spaces = child_spaces
        self.distance_function = distance_function
        self.depth = depth
        self.distance_to_proximity_weight = distance_to_proximity_weight

    @property
    def prototype(self) -> list:
        return self.location.coordinates

    def is_compatible_with(self, other: Concept) -> bool:
        return self.instance_type == other.instance_type

    def friends(self, space: Space = None) -> StructureCollection:
        space = self.parent_space if space is None else space
        if space.no_of_dimensions == 0:
            concepts = StructureCollection(
                {link.end for link in self.links_out if link.end in space.contents}
            )
            return concepts if not concepts.is_empty() else StructureCollection({self})
        return StructureCollection({self})

    def distance_from(self, other: Node):
        return self.distance_function(
            self.location_in_space(self.parent_space).coordinates,
            other.location_in_conceptual_space(self.parent_space).coordinates,
        )

    def distance_from_start(self, other: Node, end: Location = None):
        return self.distance_function(
            self.location_in_space(self.parent_space, end=end).start_coordinates,
            other.location_in_conceptual_space(self.parent_space).coordinates,
        )

    def distance_from_end(self, other: Node, start: Location = None):
        return self.distance_function(
            self.location_in_space(self.parent_space, start=start).start_coordinates,
            other.location_in_conceptual_space(self.parent_space).coordinates,
        )

    def proximity_to(self, other: Node):
        return self._distance_to_proximity(self.distance_from(other))

    def proximity_to_start(self, other: Node, end: Location = None):
        return self._distance_to_proximity(self.distance_from_start(other, end=end))

    def proximity_to_end(self, other: Node, start: Location = None):
        return self._distance_to_proximity(self.distance_from_end(other, start=start))

    def distance_between(self, a: Node, b: Node, space: "Space" = None):
        space = self.parent_space if space is None else space
        a_location = (
            a.location_in_space(space)
            if a.has_location_in_space(space)
            else a.location_in_conceptual_space(space)
        )
        b_location = (
            b.location_in_space(space)
            if b.has_location_in_space(space)
            else b.location_in_conceptual_space(space)
        )
        return self.distance_function(a_location.coordinates, b_location.coordinates)

    def proximity_between(self, a: Node, b: Node, space: "Space" = None):
        return self._distance_to_proximity(self.distance_between(a, b, space=space))

    def _distance_to_proximity(self, value: float) -> float:
        if value == 0:
            return 1.0
        inverse = 1.0 / value
        proximity = inverse * self.distance_to_proximity_weight
        return min(proximity, 1.0)
