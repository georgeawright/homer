from __future__ import annotations
from math import prod
import re
from typing import List, Union

from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.nodes import Chunk, Rule


class LetterChunk(Chunk):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: Union[str, None],
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
        abstract_chunk: LetterChunk = None,
    ):
        Chunk.__init__(
            self,
            structure_id,
            parent_id,
            locations=locations,
            members=members,
            parent_space=parent_space,
            quality=quality,
            left_branch=left_branch,
            right_branch=right_branch,
            rule=rule,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            super_chunks=super_chunks,
            abstract_chunk=abstract_chunk,
        )
        self._name = name
        self.is_letter_chunk = True

    @property
    def name(self):
        if self._name is not None:
            return self._name
        if not self.left_branch.is_empty() and not self.right_branch.is_empty():
            left_name = self.left_branch.get().name
            right_name = self.right_branch.get().name
            if left_name is None or right_name is None:
                return None
            name = f"{left_name} {right_name}"
            while "\b" in name:
                name = re.sub("[^\b]\b", "", name)
            return name
        return None

    @property
    def is_slot(self):
        return self.name is None

    @property
    def is_abstract(self):
        return self.parent_space is None

    @property
    def concepts(self):
        return self.relatives.where(is_concept=True)

    @property
    def unchunkedness(self):
        if self.is_abstract:
            return 0
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

    def nearby(self, space: Space = None) -> StructureCollection:
        if space is not None:
            return (
                space.contents.where(is_chunk=True)
                .near(self.location_in_space(space))
                .excluding(self),
            )
        return (
            self.parent_space.contents.where(is_chunk=True)
            .near(self.location_in_space(self.parent_space))
            .excluding(self)
        )

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
            chunk_copy = LetterChunk(
                structure_id=ID.new(LetterChunk),
                parent_id=parent_id,
                name=self.name,
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
                abstract_chunk=self
                if self.abstract_chunk is None
                else self.abstract_chunk,
            )
            location.space.add(chunk_copy)
            bubble_chamber.chunks.add(chunk_copy)
            bubble_chamber.loggers["structure"].log(chunk_copy)
            for member in chunk_copy.members:
                member.super_chunks.add(chunk_copy)
                bubble_chamber.loggers["structure"].log(member)
            return chunk_copy

        return copy_recursively(self, location, bubble_chamber, parent_id, {})

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
        chunk_copy = LetterChunk(
            structure_id=ID.new(LetterChunk),
            parent_id=parent_id,
            name=self.name,
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
            abstract_chunk=self if self.abstract_chunk is None else self.abstract_chunk,
        )
        bubble_chamber.loggers["structure"].log(chunk_copy)
        for member in chunk_copy.members:
            member.super_chunks.add(chunk_copy)
            bubble_chamber.loggers["structure"].log(member)
        return (chunk_copy, copies)

    def __repr__(self) -> str:
        return f'<{self.structure_id} "{self.name}" in {self.locations}>'
