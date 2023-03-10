from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluator import Evaluator
from linguoplotter.structure_collection_keys import activation


class CorrespondenceEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors import CorrespondenceSelector

        return CorrespondenceSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["correspondence"]
        view = bubble_chamber.views.get(key=activation)
        targets = bubble_chamber.new_set(
            view.members.where(start_space=view.raw_input_space).get(
                key=lambda x: abs(x.activation - x.quality)
            ),
            name="targets",
        )
        return cls.spawn(parent_id, bubble_chamber, targets, structure_type.activation)

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["correspondence"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_correspondence = self.targets.get()
        self.original_confidence = target_correspondence.quality
        start = target_correspondence.start
        end = target_correspondence.end
        argument_compatibility = (
            target_correspondence.parent_concept.classifier.classify(
                space=target_correspondence.conceptual_space,
                concept=target_correspondence.parent_concept,
                start=start,
                end=end,
                view=target_correspondence.parent_view,
            )
        )
        min_argument_quality = min(
            start.quality
            if not start.is_slot and not (start.is_link and start.start.is_slot)
            else 1.0,
            end.quality
            if not end.is_slot and not (end.is_link and end.start.is_slot)
            else 1.0,
        )
        self.confidence = argument_compatibility * min_argument_quality
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_correspondence.activation
