from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluator import Evaluator
from linguoplotter.errors import MissingStructureError


class LabelEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors import LabelSelector

        return LabelSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["label"]
        input_space = bubble_chamber.input_spaces.get()
        target = input_space.contents.filter(
            lambda x: x.is_label and not x.start.is_label
        ).get()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            bubble_chamber.new_structure_collection(target),
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["label"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_label = self.target_structures.filter(
            lambda x: x.is_label and not x.start.is_label
        ).get()
        labels = []
        while target_label is not None:
            labels.append(target_label)
            try:
                target_label = target_label.labels.get()
            except MissingStructureError:
                target_label = None
        self.confidence = fuzzy.OR(
            *[
                label.parent_concept.classifier.classify(
                    start=label.start, concept=label.parent_concept
                )
                for label in labels
            ]
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = labels[0].quality - labels[0].activation
