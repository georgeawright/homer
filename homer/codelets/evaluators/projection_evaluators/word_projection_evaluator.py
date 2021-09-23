from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import ProjectionEvaluator
from homer.structure_collection import StructureCollection


class WordProjectionEvaluator(ProjectionEvaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors.projection_selectors import WordProjectionSelector

        return WordProjectionSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["word"]
        word = bubble_chamber.input_nodes.where(is_word=True).get()
        correspondences = word.correspondences.where(end=word)
        target_structures = StructureCollection.union(
            StructureCollection({word}), correspondences
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
        target_word = self.target_structures.where(is_word=True).get()
        labels = StructureCollection.union(
            *[correspondee.labels for correspondee in target_word.correspondees]
        )
        compatible_labels = [
            label for label in labels if label.parent_concept in target_word.concepts
        ]
        self.confidence = (
            max(label.quality for label in compatible_labels)
            if compatible_labels != []
            else 1.0
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)