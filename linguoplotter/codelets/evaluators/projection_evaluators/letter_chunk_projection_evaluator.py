import statistics

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import ProjectionEvaluator
from linguoplotter.errors import MissingStructureError


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
        correspondence = self.targets.where(is_correspondence=True).get()
        view = correspondence.parent_view
        try:
            meaning_concept = letter_chunk.concepts.filter(
                lambda x: x.parent_space.name != "grammar"
            ).get()
            self.confidence = statistics.fmean(
                [
                    c.quality
                    for c in view.members
                    if c.start.parent_space in view.input_spaces
                    and c.start.is_link
                    and c.start.parent_concept == meaning_concept
                ]
            )
        except MissingStructureError:
            self.confidence = 1.0
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - letter_chunk.activation
