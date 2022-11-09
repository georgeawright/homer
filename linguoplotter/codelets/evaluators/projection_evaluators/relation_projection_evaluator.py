from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import ProjectionEvaluator


class RelationProjectionEvaluator(ProjectionEvaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors.projection_selectors import (
            RelationProjectionSelector,
        )

        return RelationProjectionSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["relation"]
        input_concept = bubble_chamber.concepts["input"]
        view = bubble_chamber.new_set(
            *[
                view
                for view in bubble_chamber.views
                if view.output_space.parent_concept == input_concept
                and view.contents.where(is_relation=True).not_empty
            ]
        ).get()
        relation = view.output_space.contents.where(is_relation=True).get()
        correspondence = relation.correspondences.where(end=relation).get()
        targets = bubble_chamber.new_set(relation, correspondence, name="targets")
        return cls.spawn(parent_id, bubble_chamber, targets, structure_type.activation)

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["relation"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        relation = self.targets.where(is_relation=True).get()
        # TODO: confidence should be confidence of items with the meaning concept
        self.confidence = 1.0
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - relation.activation
