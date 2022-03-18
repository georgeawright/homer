from __future__ import annotations
from math import prod
from typing import List

from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
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
        self._parent_space = parent_space
        self.is_raw = is_raw
        self.is_chunk = True

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "parent_id": self.parent_id,
            "locations": [str(location) for location in self.locations],
            "parent_space": self.parent_space.structure_id
            if self.parent_space is not None
            else None,
            "left_branch": [member.structure_id for member in self.left_branch],
            "right_branch": [member.structure_id for member in self.right_branch],
            "super_chunks": [member.structure_id for member in self.super_chunks],
            "quality": self.quality,
            "activation": self.activation,
        }

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
            raw_members = self.members.copy()
            raw_members.add(self)
            return raw_members
        return StructureCollection.union(
            *[chunk.raw_members for chunk in self.members.where(is_slot=False)]
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
        chunks = space.contents.where(
            is_chunk=True,
            is_letter_chunk=False,
            is_slot=False,
            parent_space=self.parent_space,
        )
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
            return bubble_chamber.new_chunk(
                parent_id=parent_id,
                locations=locations,
                parent_space=location.space,
                members=members,
                left_branch=new_left_branch,
                right_branch=new_right_branch,
                rule=chunk.rule,
                is_raw=chunk.is_raw,
                quality=0.0,
            )

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
        chunk_copy = bubble_chamber.new_chunk(
            parent_id=parent_id,
            locations=new_locations,
            parent_space=new_location.space,
            members=new_members,
            left_branch=new_left_branch,
            right_branch=new_right_branch,
            rule=self.rule,
            is_raw=self.is_raw,
            quality=self.quality,
        )
        return (chunk_copy, copies)

    def spread_activation(self):
        if not self.is_fully_active():
            return
        if self.rule is not None:
            self.rule.boost_activation(self.activation)
        if self.parent_space.is_contextual_space:
            for link in self.links:
                link.boost_activation(self.quality)
        else:
            for link in self.links_out.where(is_label=False):
                link.end.boost_activation(link.activation)
            for link in self.links_in.where(is_bidirectional=True):
                link.start.boost_activation(link.activation)

    def __repr__(self) -> str:
        members = "{" + ",".join([member.structure_id for member in self.members]) + "}"
        if self.parent_space is None:
            return f"<{self.structure_id} {members}>"
        return f"<{self.structure_id} {members} in {self.parent_space.structure_id} {self.locations}>"
