import statistics

from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import ViewEvaluator


class SimplexViewEvaluator(ViewEvaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target = bubble_chamber.simplex_views.get(
            key=lambda x: abs(x.activation - x.quality)
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            bubble_chamber.new_structure_collection(target),
            abs(target.activation - target.quality),
        )

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors.view_selectors import SimplexViewSelector

        return SimplexViewSelector

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["view-simplex"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_view = self.target_structures.get()
        self.confidence = target_view.calculate_quality()
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_view.activation
