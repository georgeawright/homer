from typing import List
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection

from .space import Space


class Link(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        start: Structure,
        end: Structure,
        locations: List[Location],
        parent_concept: "Concept",
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            locations,
            quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.start = start
        self.end = end
        self.parent_concept = parent_concept
        self.value = parent_concept.name if hasattr(parent_concept, "name") else None

    @property
    def parent_space(self) -> Space:
        return self.locations[0].space

    @property
    def arguments(self) -> StructureCollection:
        return StructureCollection(
            {arg for arg in [self.start, self.end] if arg is not None}
        )

    @property
    def is_slot(self) -> bool:
        return self.parent_concept is None

    def copy(
        self, old_arg: Structure = None, new_arg: Structure = None, parent_id: str = ""
    ):
        raise NotImplementedError

    def is_between(self, a: Structure, b: Structure):
        return self.start == a and self.end == b or self.end == a and self.start == a

    def spread_activation(self):
        if self.parent_concept is not None:
            self.parent_concept.boost_activation(self.activation)
