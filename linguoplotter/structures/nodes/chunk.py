from __future__ import annotations
from math import prod
import statistics
from typing import List

from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures import Node, Space

from .concept import Concept


class Chunk(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        locations: List[Location],
        members: StructureCollection,
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
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
            "super_chunks": [member.structure_id for member in self.super_chunks],
            "links_out": [link.structure_id for link in self.links_out],
            "links_in": [link.structure_id for link in self.links_in],
            "quality": self.quality,
            "activation": self.activation,
        }

    @classmethod
    def get_builder_class(cls):
        from linguoplotter.codelets.builders import ChunkBuilder

        return ChunkBuilder

    @classmethod
    def get_evaluator_class(cls):
        from linguoplotter.codelets.evaluators import ChunkEvaluator

        return ChunkEvaluator

    @classmethod
    def get_selector_class(cls):
        from linguoplotter.codelets.selectors import ChunkSelector

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
    def is_abstract(self):
        return self.parent_space is None

    def recalculate_unhappiness(self) -> FloatBetweenOneAndZero:
        self.recalculate_unchunkedness()
        self.recalculate_unlabeledness()
        self.recalculate_unrelatedness()
        self.recalculate_uncorrespondedness()
        return statistics.fmean(
            [
                self.unchunkedness,
                self.unlabeledness,
                self.unrelatedness,
                self.uncorrespondedness,
            ]
        )

    def recalculate_unchunkedness(self):
        if len(self.super_chunks) == 0:
            self.unchunkedness = 1
        else:
            self.unchunkedness = 0.5 * prod(
                [chunk.unchunkedness for chunk in self.super_chunks]
            )

    @property
    def potential_chunk_mates(self) -> StructureCollection:
        return self.nearby().filter(lambda x: x not in self.members)

    @property
    def adjacent(self) -> StructureCollection:
        return self.parent_space.contents.next_to(self.location).where(is_node=True)

    @property
    def is_recyclable(self) -> bool:
        return (
            self.parent_space is not None
            and self.parent_space.is_main_input
            and self.activation == 0.0
            and self.links.is_empty()
            and self.super_chunks.is_empty()
        )

    def nearby(self, space: Space = None) -> StructureCollection:
        if space is not None:
            return (
                space.contents.where(is_chunk=True)
                .near(self.location_in_space(space))
                .excluding(self),
            )
        return StructureCollection.intersection(
            *[
                location.space.contents.where(
                    is_chunk=True, parent_space=self.parent_space
                ).near(location)
                for location in self.locations
                if location.space.is_conceptual_space and location.space.is_basic_level
            ]
        ).excluding(self)

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
            return bubble_chamber.new_chunk(
                parent_id=parent_id,
                locations=locations,
                parent_space=location.space,
                members=members,
                is_raw=chunk.is_raw,
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
        chunk_copy = bubble_chamber.new_chunk(
            parent_id=parent_id,
            locations=new_locations,
            parent_space=new_location.space,
            members=new_members,
            is_raw=self.is_raw,
            quality=self.quality,
        )
        return (chunk_copy, copies)

    def __repr__(self) -> str:
        members = "{" + ",".join([member.structure_id for member in self.members]) + "}"
        if self.parent_space is None:
            return f"<{self.structure_id} {members}>"
        return f"<{self.structure_id} {members} in {self.parent_space.structure_id} {self.locations}>"
