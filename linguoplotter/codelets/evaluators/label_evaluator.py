from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluator import Evaluator


class LabelEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors import LabelSelector

        return LabelSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        input_space = bubble_chamber.input_spaces.get()
        target = input_space.contents.filter(
            lambda x: x.is_label and not x.start.is_label
        ).get(key=lambda x: abs(x.activation - x.quality))
        targets = bubble_chamber.new_set(target, name="targets")
        return cls.spawn(
            parent_id,
            bubble_chamber,
            targets,
            abs(target.activation - target.quality),
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["label"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_label = self.targets.get()
        target_node = target_label.start
        parent_concept = target_label.parent_concept
        classification = parent_concept.classifier.classify(
            concept=parent_concept, start=target_node
        )
        self.confidence = (
            classification * target_node.quality / parent_concept.number_of_components
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_label.activation
