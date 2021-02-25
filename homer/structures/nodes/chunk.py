from __future__ import annotations
from math import prod
from typing import Any, List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Link, Node, Space
from homer.tools import average_vector


class Chunk(Node):
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
        Node.__init__(
            self,
            structure_id,
            parent_id,
            value=value,
            locations=locations,
            parent_space=parent_space,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.members = members
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