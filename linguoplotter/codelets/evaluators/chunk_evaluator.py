from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.classifiers import SamenessClassifier
from linguoplotter.codelets.evaluator import Evaluator


class ChunkEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors import ChunkSelector

        return ChunkSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["chunk"]
        target = bubble_chamber.input_nodes.where(
            is_chunk=True, is_letter_chunk=False, is_raw=False, is_slot=False
        ).get()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            bubble_chamber.new_structure_collection(target),
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["chunk"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_chunk = self.target_structures.get()
        self.confidence = SamenessClassifier().classify(
            collection=target_chunk.members,
            concept=self.bubble_chamber.concepts["same"],
            spaces=target_chunk.parent_spaces.filter(
                lambda x: x.is_conceptual_space
                and x.is_basic_level
                and x.name != "size"
            ),
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = target_chunk.quality - target_chunk.activation
