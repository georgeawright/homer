from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import LabelEvaluator


class CrossViewLabelEvaluator(LabelEvaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors.label_selectors import (
            CrossViewLabelSelector,
        )

        return CrossViewLabelSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target = bubble_chamber.cross_view_labels.get(
            key=lambda x: fuzzy.OR(
                abs(x.activation - x.quality),
                bubble_chamber.worldview.view is not None
                and any(
                    [
                        x in view.output_space.contents
                        for view in bubble_chamber.worldview.view.all_sub_views
                    ]
                ),
            )
        )
        targets = bubble_chamber.new_set(target, name="targets")
        return cls.spawn(
            parent_id,
            bubble_chamber,
            targets,
            abs(target.activation - target.quality),
        )

    def _calculate_confidence(self):
        target_label = self.targets.get()
        conceptual_space = target_label.parent_spaces.filter(
            lambda x: x.is_conceptual_space and target_label.has_location_in_space(x)
        ).get()
        classification = target_label.parent_concept.classifier.classify(
            start=target_label.start,
            concept=target_label.parent_concept,
            space=conceptual_space,
        )
        self.bubble_chamber.loggers["activity"].log(f"Classification: {classification}")
        self.confidence = (
            classification / target_label.parent_concept.number_of_components
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_label.activation
