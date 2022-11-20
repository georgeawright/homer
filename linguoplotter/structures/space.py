from __future__ import annotations
import statistics

from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure import Structure
from linguoplotter.structure_collections import StructureSet


class Space(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: "Concept",
        contents: StructureSet,
        quality: FloatBetweenOneAndZero,
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
    ):
        Structure.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            locations=[],
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.name = name
        self.value = name
        self._parent_concept = parent_concept
        self.contents = contents
        self.is_space = True
        self.is_main_input = False

    def is_compatible_with(self, other: Space) -> bool:
        return self.parent_concept.is_compatible_with(other.parent_concept)

    def distance_between(self, a: Structure, b: Structure, return_nan: bool = False):
        return self.parent_concept.distance_between(
            a, b, space=self, return_nan=return_nan
        )

    def proximity_between(self, a: Structure, b: Structure, return_nan: bool = False):
        return self.parent_concept.proximity_between(
            a, b, space=self, return_nan=return_nan
        )

    def adjacency_of(self, a: Structure, b: Structure, return_nan: bool = False):
        return self.parent_concept.adjacency_of(a, b, space=self, return_nan=return_nan)

    def update_activation(self):
        self._activation = (
            statistics.median([item.activation for item in self.contents])
            if len(self.contents) != 0
            else 0.0
        )

    def spread_activation(self):
        pass

    def __repr__(self) -> str:
        return f"<{self.structure_id} {self.name}>"
