from typing import Any, Callable, List

from homer.classifier import Classifier
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.hyper_parameters import HyperParameters
from homer.id import ID
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection

from .chunk import Chunk
from .link import Link
from .space import Space


class Concept(Structure):

    DISTANCE_TO_PROXIMITY_WEIGHT = HyperParameters.DISTANCE_TO_PROXIMITY_WEIGHT

    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        location: Location,
        classifier: Classifier,
        relevant_value: str,
        child_spaces: StructureCollection,
        distance_function: Callable,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        depth: int = 1,
    ):
        quality = None
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            [location],
            quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.name = name
        self.value = name
        self.classifier = classifier
        self.relevant_value = relevant_value
        self.child_spaces = child_spaces
        self.distance_function = distance_function
        self.depth = depth

    @classmethod
    def new(
        cls,
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
        concept = cls(
            ID.new(cls),
            "",
            name,
            Location(prototype, parent_space),
            classifier,
            relevant_value,
            child_spaces,
            distance_function,
            links_in=links_in,
            links_out=links_out,
            depth=depth,
        )
        parent_space.add(concept)
        return concept

    @property
    def prototype(self) -> list:
        return self.location.coordinates

    @property
    def parent_space(self) -> Space:
        return self.location.space

    def distance_from(self, other: Structure):
        other_value = (
            other.prototype
            if isinstance(other, Concept)
            else getattr(other, self.relevant_value)
        )
        return self.distance_function(self.prototype, other_value)

    def proximity_to(self, other: Structure):
        return self._distance_to_proximity(self.distance_from(other))

    def distance_between(self, a: Structure, b: Structure):
        a_value = (
            a.prototype if isinstance(a, Concept) else getattr(a, self.relevant_value)
        )
        b_value = (
            b.prototype if isinstance(b, Concept) else getattr(b, self.relevant_value)
        )
        return self.distance_function(a_value, b_value)

    def proximity_between(self, a: Structure, b: Structure):
        return self._distance_to_proximity(self.distance_between(a, b))

    def _distance_to_proximity(self, value: float) -> float:
        if value == 0:
            return 1.0
        inverse = 1.0 / value
        proximity = inverse * self.DISTANCE_TO_PROXIMITY_WEIGHT
        return min(proximity, 1.0)
