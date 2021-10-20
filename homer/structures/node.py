from __future__ import annotations
import math
import statistics
from typing import List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection

from .space import Space


class Node(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        locations: List[Location],
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        stable_activation: FloatBetweenOneAndZero = None,
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
            stable_activation=stable_activation,
        )
        self._parent_space = parent_space
        self.is_node = True

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
    def unhappiness(self) -> FloatBetweenOneAndZero:
        return statistics.fmean(
            [
                self.unchunkedness,
                self.unlabeledness,
                self.unrelatedness,
                self.uncorrespondedness,
            ]
        )

    def nearby(self, space: Space = None) -> StructureCollection:
        raise NotImplementedError

    def get_potential_relative(
        self, space: Space = None, concept: "Concept" = None
    ) -> Node:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.structure_id} in {self.parent_space.structure_id} {self.locations}>"
