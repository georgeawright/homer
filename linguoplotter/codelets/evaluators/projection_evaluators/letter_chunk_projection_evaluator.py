from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import ProjectionEvaluator
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection import StructureCollection


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
        correspondences = word.correspondences.where(end=word)
        if correspondences.is_empty():
            raise MissingStructureError
        target_structures = StructureCollection.union(
            bubble_chamber.new_structure_collection(word), correspondences
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            target_structures,
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["letter-chunk"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        letter_chunk = self.target_structures.where(is_letter_chunk=True).get()
        self.bubble_chamber.loggers["activity"].log(
            self, f"Letter chunk: {letter_chunk} {letter_chunk.name}"
        )
        try:
            non_frame_item = (
                self.target_structures.where(is_correspondence=True)
                .filter(lambda x: not x.start.is_slot)
                .get()
                .start
            )
            frame_item = (
                self.target_structures.where(is_correspondence=True)
                .filter(lambda x: x.start.is_slot)
                .get()
                .start
            )
            correspondence_to_frame = non_frame_item.correspondences_with(
                frame_item
            ).get()
            self.confidence = fuzzy.AND(
                non_frame_item.quality, correspondence_to_frame.quality
            )
        except MissingStructureError:
            self.confidence = 1.0
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = letter_chunk.quality - letter_chunk.activation
