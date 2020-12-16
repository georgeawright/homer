from __future__ import annotations
import statistics
from typing import Any, List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.tools import average_vector

from .link import Link
from .space import Space


class Chunk(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        value: Any,
        location: Location,
        members: StructureCollection,
        neighbours: StructureCollection,
        quality: FloatBetweenOneAndZero,
        parent_spaces: StructureCollection,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            location,
            quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.value = value
        self.members = members
        self.neighbours = neighbours
        self.parent_spaces = parent_spaces

    @property
    def size(self):
        return (
            1 if len(self.members) == 0 else sum(member.size for member in self.members)
        )

    def nearby(self, space: Space = None):
        if space is not None:
            return StructureCollection.difference(
                space.contents.near(self).of_type(type(self)),
                StructureCollection({self}),
            )
        nearby_chunks = StructureCollection.union(
            *[location.space.contents.near(self) for location in self.locations]
        ).of_type(type(self))
        nearby_chunks.remove(self)
        return nearby_chunks
