from __future__ import annotations
import math

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.builder import Builder
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.id import ID
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.nodes import Chunk


class ChunkBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_structure_one = target_structures.get("target_structure_one")
        self.target_structure_two = target_structures.get("target_structure_two")
        self._target_structures = target_structures
        self.suggested_members = None

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

    @property
    def targets_dict(self):
        return {
            "target_structure_one": self.target_structure_one,
            "target_structure_two": self.target_structure_two,
        }

    def _passes_preliminary_checks(self):
        collection_one = (
            self.bubble_chamber.new_structure_collection(self.target_structure_one)
            if self.target_structure_one.members.is_empty()
            else self.target_structure_one.members
        )
        collection_two = (
            self.bubble_chamber.new_structure_collection(self.target_structure_two)
            if self.target_structure_two.members.is_empty()
            else self.target_structure_two.members
        )
        self.suggested_members = StructureCollection.union(
            collection_one, collection_two
        )
        equivalent_chunks = self.bubble_chamber.chunks.where(
            members=self.suggested_members
        )
        if not equivalent_chunks.is_empty():
            self.child_structures = self.bubble_chamber.new_structure_collection(
                equivalent_chunks.get()
            )
        return True

    def _process_structure(self):
        if not self.child_structures.is_empty():
            self.bubble_chamber.loggers["activity"].log(
                self, "Equivalent chunk already exists"
            )
            return
        chunk_locations = [
            Location.merge(
                self.target_structure_one.location_in_space(space),
                self.target_structure_two.location_in_space(space),
            )
            for space in self.target_structure_one.parent_spaces
        ]
        chunk = self.bubble_chamber.new_chunk(
            parent_id=self.codelet_id,
            locations=chunk_locations,
            members=self.suggested_members,
            parent_space=self.target_structure_one.parent_space,
            quality=0.0,
        )
        size_space = self.bubble_chamber.spaces["size"]
        chunk.location_in_space(size_space).coordinates = [[chunk.size]]
        self._structure_concept.instances.add(chunk)
        self._structure_concept.recalculate_exigency()
        self.child_structures = self.bubble_chamber.new_structure_collection(chunk)

    def _fizzle(self):
        pass
