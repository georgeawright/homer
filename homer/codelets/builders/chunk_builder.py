from __future__ import annotations

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept

from .chunk_enlarger import ChunkEnlarger


class ChunkBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        structure_concept: Concept,
        bubble_chamber: BubbleChamber,
        target_chunk: Chunk,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, urgency)
        self.structure_concept = structure_concept
        self.bubble_chamber = bubble_chamber
        self.target_chunk = target_chunk
        self.second_target_chunk = None
        self.confidence = 0.0
        self.child_structure = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_chunk: Chunk,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ""
        structure_concept = bubble_chamber.concepts["chunk"]
        return cls(
            codelet_id,
            parent_id,
            structure_concept,
            bubble_chamber,
            target_chunk,
            urgency,
        )

    def _passes_preliminary_checks(self):
        try:
            self.second_target_chunk = self.target_chunk.nearby.get_random()
        except MissingStructureError:
            return False
        return not self.bubble_chamber.has_chunk(
            StructureCollection.union(
                self.target_chunk.members,
                StructureCollection({self.second_target_chunk}),
            )
        )

    def _calculate_confidence(self):
        distances = [
            space.proximity_between(self.target_chunk, self.second_target_chunk)
            for space in self.target_chunk.parent_spaces
        ]
        self.confidence = 0.0 if distances == [] else fuzzy.AND(*distances)

    def _boost_activations(self):
        pass

    def _process_structure(self):
        new_chunk_members = StructureCollection.union(
            self.target_chunk.members,
            StructureCollection({self.second_target_chunk}),
        )
        new_chunk_neighbours = StructureCollection.union(
            self.target_chunk.neighbours, self.second_target_chunk.neighbours
        )
        new_chunk_neighbours.remove(self.target_chunk)
        new_chunk_neighbours.remove(self.second_target_chunk)
        chunk = Chunk(
            self.target_chunk.value,  # a prototype-centroid should be found
            self.target_chunk.location,  # likewise
            new_chunk_members,
            new_chunk_neighbours,
            self.target_chunk.parent_spaces,
        )
        self.bubble_chamber.add_chunk(chunk)
        self.child_structure = chunk

    def _engender_follow_up(self):
        self.child_codelets.append(
            ChunkEnlarger.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.child_structure,
                self.confidence,
            )
        )

    def _fizzle(self):
        self.child_codelets.append(
            ChunkBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_chunk,
                self.urgency / 2,
            )
        )

    def _fail(self):
        new_target = self.bubble_chamber.chunks.get_unhappy()
        self.child_codelets.append(
            ChunkBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                new_target,
                self.structure_concept.activation,
            )
        )
