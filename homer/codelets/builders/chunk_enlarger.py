from __future__ import annotations
from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Chunk
from homer.structures import Concept


class ChunkEnlarger(Builder):
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
        self.urgency = urgency
        self.candidate_member = None
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
        codelet_id = ID.new(cls)
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
            self.candidate_member = self.target_chunk.nearby.get_random()
        except MissingStructureError:
            return False
        return not self.bubble_chamber.has_chunk(
            StructureCollection.union(
                self.target_chunk.members,
                StructureCollection({self.candidate_member}),
            )
        )

    def _calculate_confidence(self):
        distances = [
            space.proximity_between(self.target_chunk, self.candidate_member)
            for space in self.target_chunk.parent_spaces
        ]
        self.confidence = 0.0 if distances == [] else fuzzy.AND(*distances)

    def _boost_activations(self):
        pass

    def _process_structure(self):
        self.target_chunk.add_member(self.candidate_member)

    def _engender_follow_up(self):
        self.child_codelets.append(
            ChunkEnlarger.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_chunk,
                self.confidence,
            )
        )

    def _fizzle(self):
        self.child_codelets.append(
            ChunkEnlarger.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_chunk,
                self.urgency / 2,
            )
        )

    def _fail(self):
        new_target = self.bubble_chamber.chunks.get_unhappy()
        self.child_codelets.append(
            ChunkEnlarger.spawn(
                self.codelet_id,
                self.bubble_chamber,
                new_target,
                self.structure_concept.activation,
            )
        )
