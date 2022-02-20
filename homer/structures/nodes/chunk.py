from __future__ import annotations
from math import prod
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
        left_branch: StructureCollection,
        right_branch: StructureCollection,
        rule: Rule,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        super_chunks: StructureCollection,
        abstract_chunk: Chunk = None,
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
            parent_spaces=parent_spaces,
        )
        self.abstract_chunk = abstract_chunk
        self.members = members
        self.left_branch = left_branch
        self.right_branch = right_branch
        self.rule = rule
        self.super_chunks = super_chunks
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
    def size(self) -> int:
        return (
            1 if len(self.members) == 0 else sum(member.size for member in self.members)
        )

    @property
    def raw_members(self) -> StructureCollection:
        if self.is_raw:
            raw_members = self.members
            raw_members.add(self)
            return raw_members
        return StructureCollection.union(*[chunk.raw_members for chunk in self.members])

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

    def nearby(self, space: Space = None) -> StructureCollection:
        if space is not None:
            return (
                space.contents.where(is_chunk=True)
                .near(self.location_in_space(space))
                .excluding(self),
            )
        return (
            StructureCollection.intersection(
                *[
                    location.space.contents.where(is_chunk=True).near(location)
                    for location in self.locations
                    if location.space.is_conceptual_space
                    and location.space.is_basic_level
                ]
            )
            # .filter(lambda x: x in self.parent_space.contents)
            .excluding(self)
        )

    def get_potential_relative(
        self, space: Space = None, concept: Concept = None
    ) -> Chunk:
        space = self.parent_space if space is None else space
        chunks = space.contents.where(is_chunk=True)
        key = lambda x: 1 - space.proximity_between(x, self)
        return chunks.get(key=key, exclude=[self])

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
            members = bubble_chamber.new_structure_collection()
            for member in chunk.members:
                if member not in copies:
                    copies[member] = copy_recursively(
                        member, location, bubble_chamber, parent_id, copies
                    )
                members.add(copies[member])
            new_left_branch = bubble_chamber.new_structure_collection(
                *[copies[member] for member in chunk.left_branch]
            )
            new_right_branch = bubble_chamber.new_structure_collection(
                *[copies[member] for member in chunk.right_branch]
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
                links_in=bubble_chamber.new_structure_collection(),
                links_out=bubble_chamber.new_structure_collection(),
                parent_spaces=bubble_chamber.new_structure_collection(
                    *[location.space for location in locations]
                ),
                super_chunks=bubble_chamber.new_structure_collection(),
                is_raw=chunk.is_raw,
            )
            location.space.contents.add(chunk_copy)
            bubble_chamber.chunks.add(chunk_copy)
            bubble_chamber.loggers["structure"].log(chunk_copy)
            for member in chunk_copy.members:
                member.super_chunks.add(chunk_copy)
                bubble_chamber.loggers["structure"].log(member)
            return chunk_copy

        return copy_recursively(self, location, bubble_chamber, parent_id, {})

    # TODO: copy with contents doesn't add item to space
    def copy_with_contents(
        self,
        copies: dict,
        bubble_chamber: "BubbleChamber",
        parent_id: str,
        new_location: Location,
    ):
        new_locations = [
            location
            for location in self.locations
            if location.space.is_conceptual_space
        ] + [new_location]
        new_members = bubble_chamber.new_structure_collection()
        for member in self.members:
            if member not in copies:
                copies[member] = member.copy(
                    copies=copies,
                    bubble_chamber=bubble_chamber,
                    parent_id=parent_id,
                    new_location=new_location,
                )
            new_members.add(copies[member])
        new_left_branch = bubble_chamber.new_structure_collection(
            *[copies[member] for member in self.left_branch]
        )
        new_right_branch = bubble_chamber.new_structure_collection(
            *[copies[member] for member in self.right_branch]
        )
        chunk_copy = Chunk(
            structure_id=ID.new(Chunk),
            parent_id=parent_id,
            locations=new_locations,
            members=new_members,
            parent_space=new_location.space,
            quality=self.quality,
            left_branch=new_left_branch,
            right_branch=new_right_branch,
            rule=self.rule,
            links_in=bubble_chamber.new_structure_collection(),
            links_out=bubble_chamber.new_structure_collection(),
            parent_spaces=bubble_chamber.new_structure_collection(
                *[location.space for location in new_locations]
            ),
            super_chunks=bubble_chamber.new_structure_collection(),
            is_raw=self.is_raw,
        )
        bubble_chamber.loggers["structure"].log(chunk_copy)
        for member in chunk_copy.members:
            member.super_chunks.add(chunk_copy)
            bubble_chamber.loggers["structure"].log(member)
        return (chunk_copy, copies)
