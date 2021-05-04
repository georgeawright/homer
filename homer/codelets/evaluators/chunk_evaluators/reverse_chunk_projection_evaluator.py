import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import ChunkEvaluator
from homer.structure_collection import StructureCollection


class ReverseChunkProjectionEvaluator(ChunkEvaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        raise NotImplementedError

    def _calculate_confidence(self):
        target_chunk = self.target_structures.where(is_chunk=True).get_random()
        parent_chunk = target_chunk.chunks_made_from_this_chunk.get_random()
        self.confidence = statistics.fmean(
            [
                link.parent_concept.classifier.classify(
                    start=target_chunk if link.start == parent_chunk else link.start,
                    end=target_chunk if link.end == parent_chunk else link.end,
                    concept=link.parent_concept,
                    space=link.parent_space,
                )
                for link in StructureCollection.union(
                    parent_chunk.labels, parent_chunk.relations
                )
            ]
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
