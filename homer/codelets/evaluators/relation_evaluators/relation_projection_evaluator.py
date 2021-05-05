from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import RelationEvaluator


class RelationProjectionEvaluator(RelationEvaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        raise NotImplementedError

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors.relation_selectors import (
            RelationProjectionSelector,
        )

        return RelationProjectionSelector

    def _calculate_confidence(self):
        target_correspondence = self.target_structures.where(
            is_correspondence=True
        ).get_random()
        self.confidence = target_correspondence.start.quality
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
