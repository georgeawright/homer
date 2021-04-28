from __future__ import annotations
from math import prod
from typing import Any, List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Node, Space


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
        is_raw: bool = False,
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
        self.is_raw = is_raw

    @classmethod
    def get_builder_class(cls):
        from homer.codelets.builders import ChunkBuilder

        return ChunkBuilder

    @classmethod
    def get_evaluator_class(cls):
        from homer.codelets.evaluators import ChunkEvaluator

        return ChunkEvaluator

    @classmethod
    def get_selector_class(cls):
        from homer.codelets.selectors import ChunkSelector

        return ChunkSelector

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
