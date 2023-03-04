from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import LabelEvaluator


class InterspatialLabelEvaluator(LabelEvaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors.label_selectors import (
            InterspatialLabelSelector,
        )

        return InterspatialLabelSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target = bubble_chamber.interspatial_labels.get(
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
        target_node = (
            target_label.start
            if not target_label.start.is_slot
            else target_label.start.non_slot_value
        )
        parent_concept = target_label.parent_concept
        space = target_label.parent_spaces.where(is_conceptual_space=True).get()
        classification = parent_concept.classifier.classify(
            concept=parent_concept, space=space, start=target_node
        )
        self.bubble_chamber.loggers["activity"].log(f"Classification: {classification}")
        self.confidence = classification / parent_concept.number_of_components
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_label.activation
