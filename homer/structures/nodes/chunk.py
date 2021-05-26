from __future__ import annotations
from math import prod
import random
from typing import Any, List

from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
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
        self.is_chunk = True

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

    def get_potential_relative(self, space: Space = None) -> Chunk:
        space = self.parent_space if space is None else space
        chunks = space.contents.where(is_chunk=True)
        if len(chunks) == 1:
            raise MissingStructureError
        for _ in range(len(chunks)):
            chunk = chunks.get_random(exclude=[self])
            if space.proximity_between(chunk, self) - random.random() <= 0:
                return chunk
        return chunks.get_random(exclude=[self])

    def copy(self, **kwargs: dict) -> Chunk:
        """Requires keyword arguments 'bubble_chamber', 'parent_id', and 'parent_space'."""
        bubble_chamber = kwargs["bubble_chamber"]
        parent_id = kwargs["parent_id"]
        parent_space = kwargs["parent_space"]
        sub_spaces = parent_space.contents.where(is_space=True)
        new_spaces = StructureCollection.union(
            sub_spaces, StructureCollection({parent_space})
        )
        locations = [
            Location(
                location.coordinates,
                [
                    space
                    for space in new_spaces
                    if space.parent_concept == location.space.parent_concept
                ][0],
            )
            for location in self.locations
        ]
        new_chunk = Chunk(
            ID.new(Chunk),
            parent_id,
            value=self.value,
            locations=locations,
            members=StructureCollection(),
            parent_space=parent_space,
            quality=self.quality,
        )
        for location in new_chunk.locations:
            location.space.add(new_chunk)
        bubble_chamber.logger.log(new_chunk)
        bubble_chamber.chunks.add(new_chunk)
        return new_chunk
