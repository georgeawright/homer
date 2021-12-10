from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import ProjectionEvaluator
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection


class LetterChunkProjectionEvaluator(ProjectionEvaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors.projection_selectors import (
            LetterChunkProjectionSelector,
        )

        return LetterChunkProjectionSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["word"]
        word = bubble_chamber.input_nodes.where(is_word=True).get()
        correspondences = word.correspondences.where(end=word)
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
        structure_concept = self.bubble_chamber.concepts["word"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
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
