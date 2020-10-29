from __future__ import annotations
from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
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
            self.candidate_member = self.target_chunk.nearby.get_random()
        except MissingPerceptletError:
            return False
        if self.target_chunk.makes_group_with(
            PerceptletCollection({self.second_target_perceptlet})
        ):
            return False
        return True

    def _calculate_confidence(self):
        common_spaces = set.intersection(
            self.target_chunk.parent_spaces, self.second_target_chunk.parent_spaces
        )
        distances = [
            space.proximity_between(self.target_chunk, self.second_target_chunk)
            for space in common_spaces
        ]
        self.confidence = 0.0 if distances == [] else fuzzy.AND(*distances)

    def _boost_activations(self):
        pass

    def _process_structure(self):
        pass

    def _engender_follow_up(self):
        return LabelBuilder()

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
        new_target = self.workspace.chunks.get_unhappy()
        self.child_codelets.append(
            ChunkBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                new_target,
                self.structure_concept.activation,
            )
        )
