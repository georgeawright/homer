from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluator import Evaluator


class RelationEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors import RelationSelector

        return RelationSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        input_space = bubble_chamber.input_spaces.get()
        target = input_space.contents.where(is_relation=True).get(
            key=lambda x: abs(x.activation - x.quality)
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            bubble_chamber.new_structure_collection(target),
            abs(target.activation - target.quality),
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["relation"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_relation = self.target_structures.get()
        self.confidence = (
            target_relation.parent_concept.classifier.classify(
                space=target_relation.conceptual_space,
                concept=target_relation.parent_concept,
                start=target_relation.start,
                end=target_relation.end,
            )
            * min(target_relation.start.quality, target_relation.end.quality)
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_relation.activation
