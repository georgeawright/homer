import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import ChunkEvaluator
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Chunk


class ChunkProjectionEvaluator(ChunkEvaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        raise NotImplementedError

    def _calculate_confidence(self):
        target_chunk = self.target_structures.where(is_chunk=True).get_random()
        self.confidence = (
            statistics.fmean([member.quality for member in target_chunk.members])
            if not target_chunk.members.is_empty()
            else 0
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
