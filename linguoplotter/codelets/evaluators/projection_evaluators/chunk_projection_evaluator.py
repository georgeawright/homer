from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import ProjectionEvaluator
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection import StructureCollection


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
        correspondences = chunk.correspondences.where(end=chunk)
        if correspondences.is_empty():
            raise MissingStructureError
        target_structures = StructureCollection.union(
            bubble_chamber.new_structure_collection(chunk), correspondences
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            target_structures,
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["chunk"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        self.confidence = 1.0
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
