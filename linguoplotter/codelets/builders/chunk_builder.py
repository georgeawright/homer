from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.builder import Builder
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.id import ID
from linguoplotter.structures.nodes import Chunk


class ChunkBuilder(Builder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators import ChunkEvaluator

        return ChunkEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_chunk: Chunk,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_chunk,
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self):
        equivalent_chunks = self.bubble_chamber.chunks.where(
            members=self.targets["members"]
        )
        if equivalent_chunks.not_empty:
            self.child_structures.add(equivalent_chunks.get())
        return True

    def _process_structure(self):
        if self.child_structures.not_empty:
            self.bubble_chamber.loggers["activity"].log(
                "Equivalent chunk already exists"
            )
            return
        chunk_locations = [
            Location.merge(
                *[
                    member.location_in_space(self.targets["node_one"].parent_space)
                    for member in self.targets["members"]
                ]
            )
        ] + [
            Location.merge(
                *[member.location_in_space(space) for member in self.targets["members"]]
            )
            for space in self.targets["node_one"].parent_space.conceptual_spaces
            if space.name != "size"
            and self.targets["node_one"].has_location_in_space(space)
        ]
        chunk = self.bubble_chamber.new_chunk(
            parent_id=self.codelet_id,
            locations=chunk_locations,
            members=self.targets["members"],
            parent_space=self.targets["node_one"].parent_space,
            quality=0.0,
        )
        for member in self.targets["members"]:
            for member_super_chunk in member.super_chunks.excluding(chunk):
                if all(
                    [c in self.targets["members"] for c in member_super_chunk.members]
                ):
                    chunk.sub_chunks.add(member_super_chunk)
                    member_super_chunk.super_chunks.add(chunk)
            member.super_chunks.add(chunk)
        self._structure_concept.instances.add(chunk)
        self._structure_concept.recalculate_salience()
        self.child_structures.add(chunk)

    def _fizzle(self):
        pass
