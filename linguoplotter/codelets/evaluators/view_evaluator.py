from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluator import Evaluator


class ViewEvaluator(Evaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target = bubble_chamber.views.get(key=lambda x: abs(x.activation - x.quality))
        targets = bubble_chamber.new_set(target, name="targets")
        return cls.spawn(
            parent_id,
            bubble_chamber,
            targets,
            abs(target.activation - target.quality),
        )

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors import ViewSelector

        return ViewSelector

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["view"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_view = self.targets.get()
        self.confidence = target_view.calculate_quality()
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_view.activation
