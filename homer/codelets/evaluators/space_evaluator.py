import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator


class SpaceEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors import SpaceSelector

        return SpaceSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["conceptual-space"]
        target = bubble_chamber.conceptual_spaces.get()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            bubble_chamber.new_structure_collection(target),
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["conceptual-space"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_space = self.target_structures.get()
        self.confidence = statistics.median(
            *[label.quality for label in target_space.contents.where(is_label=True)]
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
