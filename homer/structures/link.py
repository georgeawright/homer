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
        self._parent_concept = parent_concept
        self.value = parent_concept.name if hasattr(parent_concept, "name") else None
        self.is_link = True

    @property
    def parent_space(self) -> Space:
        contextual_spaces = [
            location.space
            for location in self.locations
            if location.space.is_contextual_space
        ]
        return contextual_spaces[0] if len(contextual_spaces) > 0 else None

    @property
    def arguments(self) -> StructureCollection:
        return StructureCollection(
            {arg for arg in [self.start, self.end] if arg is not None}
        )

    @property
    def is_slot(self) -> bool:
        return self.parent_concept is None

    def is_between(self, a: Structure, b: Structure):
        return self.start == a and self.end == b or self.end == a and self.start == a

    def spread_activation(self):
        if self.parent_concept is not None:
            self.parent_concept.boost_activation(self.activation)

    def __repr__(self) -> str:
        concept = "none" if self.parent_concept is None else self.parent_concept.name
        args = ", ".join([arg.structure_id for arg in self.arguments])
        spaces = ", ".join([location.space.name for location in self.locations])
        return f"<{self.structure_id} {concept}({args}) in {spaces}>"
