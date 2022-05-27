from typing import List
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.structure import Structure
from linguoplotter.structure_collection import StructureCollection

from .space import Space


class Link(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        start: Structure,
        end: Structure,
        arguments: StructureCollection,
        locations: List[Location],
        parent_concept: "Concept",
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            locations,
            quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
        )
        self.start = start
        self.end = end
        self.arguments = arguments
        self._parent_concept = parent_concept
        self.value = parent_concept.name if hasattr(parent_concept, "name") else None
        self.is_excitatory = True
        self.is_link = True

    @property
    def parent_space(self) -> Space:
        return self._parent_space

    @property
    def is_slot(self) -> bool:
        return self.parent_concept.is_slot

    @property
    def is_recyclable(self) -> bool:
        return (
            self.parent_space is not None
            and self.parent_space.is_main_input
            and self.activation == 0.0
            and self.links.is_empty()
        )

    def recalculate_unlabeledness(self):
        self.unlabeledness = 0.5 * 0.5 ** sum(link.activation for link in self.labels)

    def recalculate_unrelatedness(self):
        self.unrelatedness = 0.5 * 0.5 ** sum(
            link.activation for link in self.relations
        )

    def is_between(self, a: Structure, b: Structure):
        return self.start == a and self.end == b or self.end == a and self.start == a

    def spread_activation(self):
        if not self.is_fully_active:
            return
        if (
            self.start.parent_space is None
            or self.start.parent_space.is_conceptual_space
        ):
            return
        if self.parent_concept is not None:
            self.parent_concept.boost_activation(self.quality)
        for argument in self.arguments.filter(
            lambda x: x.parent_space is not None and x.parent_space.is_contextual_space
        ):
            argument.boost_activation(self.quality)

    def __repr__(self) -> str:
        concept = "none" if self.parent_concept is None else self.parent_concept.name
        args = f"{self.start.structure_id}"
        if self.end is not None:
            args += f", {self.end.structure_id}"
        spaces = ", ".join([location.space.name for location in self.locations])
        return f"<{self.structure_id} {concept}({args}) in {spaces}>"
