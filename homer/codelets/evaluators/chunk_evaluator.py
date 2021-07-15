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
        target = bubble_chamber.input_nodes.where(is_chunk=True).get()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({target}),
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["chunk"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_chunk = self.target_structures.where(is_slot=False).get()
        if target_chunk.rule.right_concept is None:
            self.confidence = target_chunk.rule.left_concept.classifier.classify_chunk(
                root=target_chunk, child=None
            )
        else:
            self.confidence = statistics.fmean(
                [
                    target_chunk.rule.left_concept.classifier.classify_chunk(
                        root=target_chunk,
                        child=target_chunk.left_branch.get(),
                    ),
                    target_chunk.rule.right_concept.classifier.classify_chunk(
                        root=target_chunk,
                        child=target_chunk.right_branch.get(),
                    ),
                ]
            )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
