from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import ProjectionEvaluator


class LetterChunkProjectionEvaluator(ProjectionEvaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors.projection_selectors import (
            LetterChunkProjectionSelector,
        )

        return LetterChunkProjectionSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["letter-chunk"]
        word = bubble_chamber.input_nodes.where(is_letter_chunk=True).get()
        correspondence = word.correspondences.where(end=word).get()
        targets = bubble_chamber.new_set(word, correspondence, name="targets")
        return cls.spawn(parent_id, bubble_chamber, targets, structure_type.activation)

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["letter-chunk"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        letter_chunk = self.targets.where(is_letter_chunk=True).get()
        # TODO: confidence should be confidence of items with the meaning concept
        self.confidence = 1.0
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - letter_chunk.activation
