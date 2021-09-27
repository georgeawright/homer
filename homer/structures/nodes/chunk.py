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
from homer.structures.spaces import ContextualSpace

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
        left_branch: StructureCollection = None,
        right_branch: StructureCollection = None,
        rule: Rule = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        super_chunks: StructureCollection = None,
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
        self.left_branch = (
            left_branch if left_branch is not None else StructureCollection()
        )
        self.right_branch = (
            right_branch if right_branch is not None else StructureCollection()
        )
        self.rule = rule
        self.super_chunks = (
            super_chunks if super_chunks is not None else StructureCollection()
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
        if len(self.super_chunks) == 0:
            return 1
        return 0.5 * prod([chunk.unchunkedness for chunk in self.super_chunks])

    @property
    def free_branch_concept(self):
        if self.rule.root_concept == self.rule.left_concept:
            return self.rule.left_concept
        if self.left_branch.is_empty():
            return self.rule.left_concept
        if self.right_branch.is_empty() and self.rule.right_concept is not None:
            return self.rule.right_concept
        raise MissingStructureError

    @property
    def free_branch(self):
        if self.rule.root_concept == self.rule.left_concept:
            return self.left_branch
        if self.left_branch.is_empty():
            return self.left_branch
        if self.right_branch.is_empty() and self.rule.right_concept is not None:
            return self.right_branch
        raise MissingStructureError

    @property
    def has_free_branch(self):
        try:
            return self.free_branch is not None
        except MissingStructureError:
            return False

    @property
    def potential_chunk_mates(self) -> StructureCollection:
        return StructureCollection.union(self.adjacent, self.super_chunks, self.members)

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

    def copy_to_location(
        self, location: Location, bubble_chamber: "BubbleChamber", parent_id: str = ""
    ):
        def copy_recursively(
            chunk: Chunk,
            location: Location,
            bubble_chamber: "BubbleChamber",
            parent_id: str,
            copies: dict,
        ):
            locations = [
                location
                for location in chunk.locations
                if location.space.is_conceptual_space
            ] + [location]
            members = StructureCollection()
            for member in chunk.members:
                if member not in copies:
                    copies[member] = copy_recursively(
                        member, location, bubble_chamber, parent_id, copies
                    )
                members.add(copies[member])
            new_left_branch = StructureCollection(
                {copies[member] for member in chunk.left_branch}
            )
            new_right_branch = StructureCollection(
                {copies[member] for member in chunk.right_branch}
            )
            chunk_copy = Chunk(
                structure_id=ID.new(Chunk),
                parent_id=parent_id,
                locations=locations,
                members=members,
                parent_space=location.space,
                quality=0.0,
                left_branch=new_left_branch,
                right_branch=new_right_branch,
                rule=chunk.rule,
                is_raw=chunk.is_raw,
            )
            location.space.contents.add(chunk_copy)
            bubble_chamber.chunks.add(chunk_copy)
            bubble_chamber.logger.log(chunk_copy)
            for member in chunk_copy.members:
                member.super_chunks.add(chunk_copy)
                bubble_chamber.logger.log(member)
            return chunk_copy

        return copy_recursively(self, location, bubble_chamber, parent_id, {})

    # TODO: get rid of
    def copy_with_contents(
        self,
        copies: dict,
        bubble_chamber: "BubbleChamber",
        parent_id: str,
        parent_space: ContextualSpace,
    ):
        new_locations = [
            location
            for location in self.locations
            if location.space.is_conceptual_space
        ]
        new_locations.append(
            Location(
                self.location_in_space(self.parent_space).coordinates, parent_space
            )
        )
        new_members = StructureCollection()
        for member in self.members:
            if member not in copies:
                copies[member] = member.copy(
                    copies=copies,
                    bubble_chamber=bubble_chamber,
                    parent_id=parent_id,
                    parent_space=parent_space,
                )
            new_members.add(copies[member])
        new_left_branch = StructureCollection(
            {copies[member] for member in self.left_branch}
        )
        new_right_branch = StructureCollection(
            {copies[member] for member in self.right_branch}
        )
        chunk_copy = Chunk(
            structure_id=ID.new(Chunk),
            parent_id=parent_id,
            locations=new_locations,
            members=new_members,
            parent_space=parent_space,
            quality=self.quality,
            left_branch=new_left_branch,
            right_branch=new_right_branch,
            rule=self.rule,
            is_raw=self.is_raw,
        )
        bubble_chamber.logger.log(chunk_copy)
        for member in chunk_copy.members:
            member.super_chunks.add(chunk_copy)
            bubble_chamber.logger.log(member)
        return (chunk_copy, copies)
