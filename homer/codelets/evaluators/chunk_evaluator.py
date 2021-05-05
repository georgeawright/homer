import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator
from homer.structure_collection import StructureCollection


class ChunkEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors import ChunkSelector

        return ChunkSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["chunk"]
        target = bubble_chamber.chunks.get_random()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({target}),
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["chunk"]
        return structure_concept.relations_with(self._evaluate_concept).get_random()

    def _calculate_confidence(self):
        target_chunk = self.target_structures.get_random()
        proximities = [
            space.proximity_between(member, target_chunk)
            for space in target_chunk.parent_spaces
            for member in target_chunk.members
            if space.is_basic_level
        ]
        self.confidence = statistics.fmean(proximities) if proximities != [] else 0
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
