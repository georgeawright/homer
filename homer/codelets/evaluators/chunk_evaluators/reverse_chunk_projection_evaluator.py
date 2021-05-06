import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import ChunkEvaluator
from homer.structure_collection import StructureCollection


class ReverseChunkProjectionEvaluator(ChunkEvaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target_view = bubble_chamber.monitoring_views.get_active()
        target_chunk = target_view.interpretation_space.contents.where(
            is_chunk=True, members=StructureCollection()
        ).get_random()
        target_correspondence = target_chunk.correspondences_to_space(
            target_view.raw_input_space
        ).get_random()
        target_structures = StructureCollection({target_chunk, target_correspondence})
        urgency = statistics.fmean(
            [
                concept.activation
                for concept in [
                    bubble_chamber.concepts["chunk"],
                    bubble_chamber.concepts["outer"],
                    bubble_chamber.concepts["reverse"],
                    bubble_chamber.concepts["evaluate"],
                ]
            ]
        )
        return cls.spawn(parent_id, bubble_chamber, target_structures, urgency)

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors.chunk_selectors import (
            ReverseChunkProjectionSelector,
        )

        return ReverseChunkProjectionSelector

    def _calculate_confidence(self):
        target_chunk = self.target_structures.where(
            is_chunk=True, members=StructureCollection()
        ).get_random()
        parent_chunk = target_chunk.chunks_made_from_this_chunk.get_active()
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