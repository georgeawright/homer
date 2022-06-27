from __future__ import annotations
from math import prod
import re
from typing import List, Union

from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures import Space
from linguoplotter.structures.nodes import Chunk


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
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        super_chunks: StructureCollection,
        containing_chunks: StructureCollection,
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
            super_chunks=super_chunks,
            containing_chunks=containing_chunks,
            abstract_chunk=abstract_chunk,
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
            "links_out": [link.structure_id for link in self.links_out],
            "links_in": [link.structure_id for link in self.links_in],
            "quality": self.quality,
            "activation": self.activation,
        }

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

    def recalculate_unchunkedness(self):
        if self.is_abstract:
            self.unchunkedness = 0
        elif len(self.containing_chunks) == 0:
            self.unchunkedness = 1
        else:
            self.unchunkedness = 0.5 * prod(
                [chunk.unchunkedness for chunk in self.containing_chunks]
            )

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
                location.copy()
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
            return bubble_chamber.new_letter_chunk(
                parent_id=parent_id,
                name=self.name,
                locations=locations,
                members=members,
                parent_space=location.space,
                left_branch=new_left_branch,
                right_branch=new_right_branch,
                abstract_chunk=self
                if self.abstract_chunk is None
                else self.abstract_chunk,
                quality=0.0,
            )

        return copy_recursively(self, location, bubble_chamber, parent_id, {})

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
        left = (
            self.left_branch.get().structure_id
            if not self.left_branch.is_empty()
            else ""
        )
        right = (
            self.right_branch.get().structure_id
            if not self.right_branch.is_empty()
            else ""
        )
        members = ",".join([left, right])
        return f'<{self.structure_id} "{self.name}" [{members}] in {self.locations}>'
