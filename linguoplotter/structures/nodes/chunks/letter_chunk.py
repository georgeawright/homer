from __future__ import annotations
from math import prod
import re
from typing import List, Union

from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures import Space
from linguoplotter.structures.nodes import Chunk


class LetterChunk(Chunk):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: Union[str, None],
        locations: List[Location],
        members: StructureSet,
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        left_branch: StructureSet,
        right_branch: StructureSet,
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        instances: StructureSet,
        super_chunks: StructureSet,
        sub_chunks: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
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
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            instances=instances,
            super_chunks=super_chunks,
            sub_chunks=sub_chunks,
            abstract_chunk=abstract_chunk,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.left_branch = left_branch
        self.right_branch = right_branch
        self._name = name
        self.is_letter_chunk = True

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "locations": [str(location) for location in self.locations],
            "parent_space": self.parent_space.structure_id
            if self.parent_space is not None
            else None,
            "left_branch": [member.structure_id for member in self.left_branch],
            "right_branch": [member.structure_id for member in self.right_branch],
            "super_chunks": [member.structure_id for member in self.super_chunks],
            "sub_chunks": [member.structure_id for member in self.sub_chunks],
            "links_out": [link.structure_id for link in self.links_out],
            "links_in": [link.structure_id for link in self.links_in],
            "quality": self.quality,
            "activation": self.activation,
        }

    @property
    def name(self):
        if self._name is not None:
            return self._name
        if self.left_branch.not_empty and self.right_branch.not_empty:
            left_name = self.left_branch.get().name
            right_name = self.right_branch.get().name
            if left_name is None or right_name is None:
                return None
            name = f"{left_name} {right_name}"
            while "[b]" in name:
                name = re.sub(r"\[b\]", "\b", name)
            return " ".join(name.split())
        return None

    @property
    def is_slot(self):
        return self.name is None

    @property
    def concepts(self):
        return self.relatives.where(is_concept=True)

    @property
    def most_super_chunk(self) -> LetterChunk:
        if self.super_chunks.is_empty:
            raise MissingStructureError
        try:
            return self.super_chunks.get().most_super_chunk
        except MissingStructureError:
            return self.super_chunks.get()

    @property
    def left_neighbour(self):
        super_chunk = self.super_chunks.get()
        if self in super_chunk.right_branch:
            return super_chunk.left_branch.get().rightmost_child
        if self in super_chunk.left_branch:
            return super_chunk.left_neighbour

    @property
    def right_neighbour(self):
        super_chunk = self.super_chunks.get()
        if self in super_chunk.left_branch:
            return super_chunk.right_branch.get().leftmost_child
        if self in super_chunk.right_branch:
            return super_chunk.right_neighbour

    @property
    def leftmost_child(self):
        if self.members.is_empty:
            return self
        return self.left_branch.get().leftmost_child

    @property
    def rightmost_child(self):
        if self.members.is_empty:
            return self
        if self.right_branch.not_empty:
            return self.right_branch.get().rightmost_child
        return self.left_branch.get().rightmost_child

    def lowest_common_ancestor_with(self, other: LetterChunk) -> LetterChunk:
        def path_to_root(child):
            path = []
            super_chunk = child
            while True:
                path.append(super_chunk)
                try:
                    super_chunk = super_chunk.super_chunks.get()
                except MissingStructureError:
                    break
            path.reverse()
            return path

        self_path_to_root = path_to_root(self)
        other_path_to_root = path_to_root(other)
        lowest_common_ancestor = None
        for s, o in zip(self_path_to_root, other_path_to_root):
            if s == o:
                lowest_common_ancestor = s
            if s != o:
                break
        return lowest_common_ancestor

    def is_to_the_left_of(self, other: LetterChunk) -> bool:
        common_ancestor = self.lowest_common_ancestor_with(other)
        if common_ancestor is None:
            return False
        uncommon_ancestor = self
        while True:
            super_chunk = uncommon_ancestor.super_chunks.get()
            if super_chunk != common_ancestor:
                uncommon_ancestor = super_chunk
            else:
                break
        return uncommon_ancestor in common_ancestor.left_branch

    def update_string_location(self):
        not_none = False
        if self.structure_id == "LetterChunk569" and self.name is not None:
            not_none = True
        for location in self.locations:
            if location.space.name != "string":
                continue
            location.coordinates = [[self.name]]
        if self.structure_id == "LetterChunk569" and self.name is None and not_none:
            raise Exception
        for super_chunk in self.super_chunks:
            super_chunk.update_string_location()

    def recalculate_unchunkedness(self):
        if self.is_abstract:
            self.unchunkedness = 0
        elif len(self.super_chunks) == 0:
            self.unchunkedness = 1
        else:
            self.unchunkedness = 0.5 * prod(
                [chunk.unchunkedness for chunk in self.super_chunks]
            )

    def nearby(self, space: Space = None) -> StructureSet:
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

    def copy_with_contents(
        self,
        copies: dict,
        bubble_chamber: "BubbleChamber",
        parent_id: str,
        new_location: Location,
    ):
        new_locations = [
            location.copy()
            for location in self.locations
            if location.space.is_conceptual_space
        ] + [new_location]
        new_members = bubble_chamber.new_set()
        for member in self.members:
            if member not in copies:
                copies[member], copies = member.copy_with_contents(
                    copies=copies,
                    bubble_chamber=bubble_chamber,
                    parent_id=parent_id,
                    new_location=new_location,
                )
            new_members.add(copies[member])
        new_left_branch = bubble_chamber.new_set(
            *[copies[member] for member in self.left_branch]
        )
        new_right_branch = bubble_chamber.new_set(
            *[copies[member] for member in self.right_branch]
        )
        chunk_copy = bubble_chamber.new_letter_chunk(
            parent_id=parent_id,
            name=self.name,
            locations=new_locations,
            members=new_members,
            parent_space=new_location.space,
            left_branch=new_left_branch,
            right_branch=new_right_branch,
            abstract_chunk=self if self.abstract_chunk is None else self.abstract_chunk,
            quality=self.quality,
        )
        return (chunk_copy, copies)

    def __repr__(self) -> str:
        left = self.left_branch.get().structure_id if self.left_branch.not_empty else ""
        right = (
            self.right_branch.get().structure_id if self.right_branch.not_empty else ""
        )
        members = ",".join([left, right])
        return f'<{self.structure_id} "{self.name}" [{members}] in {self.locations}>'
