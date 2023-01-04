from __future__ import annotations
import math
from typing import List

from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.structure import Structure
from linguoplotter.structure_collections import StructureSet

from .space import Space


class Node(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        locations: List[Location],
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        instances: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
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
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.instances = instances
        self._parent_space = parent_space
        self.is_node = True
        self._non_slot_value = None

    @property
    def parent_space(self) -> Space:
        return self._parent_space

    @parent_space.setter
    def parent_space(self, space: Space):
        self._parent_space = space

    @property
    def is_slot(self):
        return any(
            [
                math.nan in coordinates
                for location in self.locations
                for coordinates in location.coordinates
            ]
        )

    @property
    def is_filled_in(self) -> bool:
        return self.non_slot_value is not None

    @property
    def non_slot_value(self) -> Node:
        if self._non_slot_value is None:
            return None
        if not self._non_slot_value.is_slot:
            return self._non_slot_value
        return self._non_slot_value.non_slot_value

    def recalculate_uncorrespondedness(self):
        self.uncorrespondedness = 0.5 * 0.5 ** sum(
            link.activation for link in self.correspondences
        )

    def nearby(self, space: Space = None) -> StructureSet:
        raise NotImplementedError

    def __repr__(self) -> str:
        if self.parent_space is None:
            return f"<{self.structure_id}>"
        return f"<{self.structure_id} in {self.parent_space.structure_id} {self.locations}>"
