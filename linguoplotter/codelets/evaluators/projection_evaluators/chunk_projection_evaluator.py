from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import ProjectionEvaluator


class ChunkProjectionEvaluator(ProjectionEvaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors.projection_selectors import (
            ChunkProjectionSelector,
        )

        return ChunkProjectionSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["chunk"]
        chunk = bubble_chamber.input_nodes.where(is_chunk=True).get()
        correspondence = chunk.correspondences.where(end=chunk).get()
        targets = bubble_chamber.new_set(chunk, correspondence, name="targets")
        return cls.spawn(parent_id, bubble_chamber, targets, structure_type.activation)

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["chunk"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        chunk = self.targets.where(is_chunk=True).get()
        self.confidence = 1.0
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - chunk.activation
