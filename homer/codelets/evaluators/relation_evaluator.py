from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator


class RelationEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors import RelationSelector

        return RelationSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["relation"]
        target = bubble_chamber.relations.get()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            bubble_chamber.new_structure_collection(target),
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["relation"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_relation = self.target_structures.get()
        self.confidence = target_relation.parent_concept.classifier.classify(
            space=target_relation.parent_space,
            concept=target_relation.parent_concept,
            start=target_relation.start,
            end=target_relation.end,
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
