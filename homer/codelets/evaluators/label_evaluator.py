from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator
from homer.structure_collection import StructureCollection


class LabelEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors import LabelSelector

        return LabelSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["label"]
        target = bubble_chamber.labels.get()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({target}),
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["label"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_label = self.target_structures.get()
        self.confidence = target_label.parent_concept.classifier.classify(
            start=target_label.start,
            concept=target_label.parent_concept,
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
