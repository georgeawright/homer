from __future__ import annotations
from math import prod
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
        locations: List[Location],
        members: StructureCollection,
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        chunks_made_from_this_chunk: StructureCollection = None,
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
        self.value = value
        self.members = members
        self.parent_space = parent_space
        self.chunks_made_from_this_chunk = (
            chunks_made_from_this_chunk
            if chunks_made_from_this_chunk is not None
            else StructureCollection()
        )

    @property
    def size(self):
        return (
            1 if len(self.members) == 0 else sum(member.size for member in self.members)
        )

    @property
    def unchunkedness(self):
        if len(self.chunks_made_from_this_chunk) == 0:
            return 1
        return 0.5 * prod(
            [chunk.unchunkedness for chunk in self.chunks_made_from_this_chunk]
        )

    def nearby(self, space: Space = None):
        if space is not None:
            return StructureCollection.difference(
                space.contents.near(self.location_in_space(space)).of_type(type(self)),
                StructureCollection({self}),
            )
        nearby_chunks = StructureCollection.union(
            *[location.space.contents.near(location) for location in self.locations]
        ).of_type(type(self))
        nearby_chunks.remove(self)
        return nearby_chunks
