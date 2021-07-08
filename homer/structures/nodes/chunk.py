from __future__ import annotations
from math import prod
import random
from typing import List

from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Node, Space

from .concept import Concept
from .rule import Rule


class Chunk(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        locations: List[Location],
        members: StructureCollection,
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        left_branch: Node = None,
        right_branch: Node = None,
        rule: Rule = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        chunks_made_from_this_chunk: StructureCollection = None,
        is_raw: bool = False,
    ):
        Node.__init__(
            self,
            structure_id,
            parent_id,
            locations=locations,
            parent_space=parent_space,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.members = members
        self.left_branch = left_branch
        self.right_branch = right_branch
        self.rule = rule
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

    @property
    def potential_chunk_mates(self) -> StructureCollection:
        return StructureCollection.union(
            self.adjacent, self.chunks_made_from_this_chunk, self.members
        )

    @property
    def adjacent(self) -> StructureCollection:
        return self.parent_space.contents.next_to(self.location).where(is_node=True)

    def get_potential_relative(
        self, space: Space = None, concept: Concept = None
    ) -> Chunk:
        space = self.parent_space if space is None else space
        chunks = space.contents.where(is_chunk=True)
        if len(chunks) == 1:
            raise MissingStructureError
        for _ in range(len(chunks)):
            chunk = chunks.get(exclude=[self])
            if space.proximity_between(chunk, self) - random.random() <= 0:
                return chunk
        return chunks.get(exclude=[self])

    def nearby(self, space: Space = None) -> StructureCollection:
        pass

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
