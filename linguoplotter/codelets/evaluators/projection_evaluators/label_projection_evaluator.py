import statistics

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import ProjectionEvaluator


class LabelProjectionEvaluator(ProjectionEvaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors.projection_selectors import (
            LabelProjectionSelector,
        )

        return LabelProjectionSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["label"]
        input_concept = bubble_chamber.concepts["input"]
        view = bubble_chamber.new_set(
            *[
                view
                for view in bubble_chamber.views
                if view.output_space.parent_concept == input_concept
                and view.contents.where(is_label=True).not_empty
            ]
        ).get()
        label = view.ouptut_space.contents.where(is_label=True).get()
        correspondence = label.correspondences.where(end=label).get()
        targets = bubble_chamber.new_set(label, correspondence, name="targets")
        return cls.spawn(parent_id, bubble_chamber, targets, structure_type.activation)

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["label"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        label = self.targets.where(is_label=True).get()
        correspondence = self.targets.where(is_correspondence=True).get()
        view = correspondence.parent_view
        try:
            self.confidence = statistics.fmean(
                [
                    c.quality
                    for c in view.members
                    if c.start.parent_space in view.input_spaces
                    and c.start.is_link
                    and c.start.parent_concept == label.parent_concept
                ]
            )
        except statistics.StatisticsError:
            self.confidence = 1.0
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - label.activation
