from __future__ import annotations
from typing import Callable, List

from homer.classifier import Classifier
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
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
        structure_type: type,
        parent_space: Space,
        child_spaces: StructureCollection,
        distance_function: Callable,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
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
            parent_spaces=parent_spaces,
        )
        self.name = name
        self.classifier = classifier
        self.instance_type = instance_type
        self.structure_type = structure_type
        self.child_spaces = child_spaces
        self.distance_function = distance_function
        self.depth = depth
        self.distance_to_proximity_weight = distance_to_proximity_weight
        self.is_concept = True

    @property
    def prototype(self) -> list:
        return self.location.coordinates

    def letter_chunk_forms(
        self, grammar_concept: Concept = None
    ) -> StructureCollection:
        return StructureCollection.union(
            *[
                link.arguments.excluding(self)
                for link in self.links_out.filter(
                    lambda x: x.end.is_word
                    and (
                        x.parent_concept == grammar_concept
                        if grammar_concept is not None
                        else True
                    )
                )
            ]
        )

    def compatibility_with(self, other: Concept) -> FloatBetweenOneAndZero:
        if (
            self == other
            or self.parent_space.parent_concept == other
            or other.parent_space.parent_concept == self
        ):
            return 1.0
        if self.parent_space == other.parent_space:
            return self.proximity_to(other)
        return 0.0

    def friends(self, space: Space = None) -> StructureCollection:
        space = self.parent_space if space is None else space
        friend_concepts = self.relatives.filter(lambda x: x in space.contents)
        if friend_concepts.is_empty():
            friend_concepts.add(self)
        return friend_concepts

    def distance_from(self, other: Node):
        return self.distance_function(
            self.location_in_space(self.parent_space).coordinates,
            other.location_in_space(self.parent_space).coordinates,
        )

    def distance_from_start(self, other: Node, end: Location = None):
        return self.distance_function(
            self.location_in_space(self.parent_space, end=end).start_coordinates,
            other.location_in_space(self.parent_space).coordinates,
        )

    def distance_from_end(self, other: Node, start: Location = None):
        return self.distance_function(
            self.location_in_space(self.parent_space, start=start).end_coordinates,
            other.location_in_space(self.parent_space).coordinates,
        )

    def proximity_to(self, other: Node):
        return self._distance_to_proximity(self.distance_from(other))

    def proximity_to_start(self, other: Node, end: Location = None):
        return self._distance_to_proximity(self.distance_from_start(other, end=end))

    def proximity_to_end(self, other: Node, start: Location = None):
        return self._distance_to_proximity(self.distance_from_end(other, start=start))

    def distance_between(self, a: Node, b: Node, space: "Space" = None):
        space = self.parent_space if space is None else space
        return self.distance_function(
            a.location_in_space(space).coordinates,
            b.location_in_space(space).coordinates,
        )

    def proximity_between(self, a: Node, b: Node, space: "Space" = None):
        return self._distance_to_proximity(self.distance_between(a, b, space=space))

    def _distance_to_proximity(self, value: float) -> float:
        # TODO: consider using a distance_to_proximity function instead of weight
        if value == 0:
            return 1.0
        # return min(self.distance_to_proximity_function(value), 1.0)
        inverse = 1.0 / value
        proximity = inverse * self.distance_to_proximity_weight
        return min(proximity, 1.0)

    def __repr__(self) -> str:
        return (
            f"<{self.structure_id} {self.name} in "
            + f"{self.parent_space.structure_id} {self.locations}>"
        )
