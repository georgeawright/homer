from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator


class ChunkEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors import ChunkSelector

        return ChunkSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["chunk"]
        target = bubble_chamber.input_nodes.where(
            is_chunk=True, is_letter_chunk=False, is_raw=False
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
        target_chunk = self.target_structures.where(is_slot=False).get()
        classifications = [
            target_chunk.rule.left_concept.classifier.classify(
                collection=target_chunk.left_branch.where(is_slot=False),
                concept=target_chunk.rule.left_concept,
            ),
        ]
        if target_chunk.rule.right_concept is not None:
            classifications.append(
                target_chunk.rule.right_concept.classifier.classify(
                    collection=target_chunk.right_branch.where(is_slot=False),
                    concept=target_chunk.rule.right_concept,
                ),
            )
        self.confidence = fuzzy.AND(*classifications)
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
