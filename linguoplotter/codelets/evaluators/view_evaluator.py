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
        if target_view.members.filter(
            lambda x: x.end not in target_view.output_space.contents
        ).is_empty:
            progenitor = target_view.parent_frame.progenitor
            number_of_equivalent_views = len(
                self.bubble_chamber.views.filter(
                    lambda x: x.parent_frame.progenitor == progenitor
                    and x.unhappiness > 0
                )
            )
            self.confidence = progenitor.activation * 0.5**number_of_equivalent_views
        else:
            self.confidence = target_view.calculate_quality()
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_view.activation
