import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import ChunkEvaluator
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation


class ChunkProjectionEvaluator(ChunkEvaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target_view = bubble_chamber.monitoring_views.get(key=activation)
        target_chunk = (
            target_view.interpretation_space.contents.where(is_chunk=True)
            .where_not(members=StructureCollection())
            .get()
        )
        target_correspondence = target_chunk.correspondences_to_space(
            target_view.text_space
        ).get()
        target_structures = StructureCollection({target_chunk, target_correspondence})
        urgency = statistics.fmean(
            [
                concept.activation
                for concept in [
                    bubble_chamber.concepts["chunk"],
                    bubble_chamber.concepts["outer"],
                    bubble_chamber.concepts["forward"],
                    bubble_chamber.concepts["evaluate"],
                ]
            ]
        )
        return cls.spawn(parent_id, bubble_chamber, target_structures, urgency)

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors.chunk_selectors import ChunkProjectionSelector

        return ChunkProjectionSelector

    def _calculate_confidence(self):
        target_chunk = self.target_structures.where(is_chunk=True).get()
        self.confidence = (
            statistics.fmean([member.quality for member in target_chunk.members])
            if not target_chunk.members.is_empty()
            else 0
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
