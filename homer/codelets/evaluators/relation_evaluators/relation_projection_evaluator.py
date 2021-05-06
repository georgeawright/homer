import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import RelationEvaluator
from homer.structure_collection import StructureCollection


class RelationProjectionEvaluator(RelationEvaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target_view = bubble_chamber.monitoring_views.get_active()
        target_relation = target_view.interpretation_space.contents.where(
            is_relation=True
        ).get_random()
        target_correspondence = target_relation.correspondences_to_space(
            target_view.text_space
        ).get_random()
        target_structures = StructureCollection(
            {target_relation, target_correspondence}
        )
        urgency = statistics.fmean(
            [
                concept.activation
                for concept in [
                    bubble_chamber.concepts["relation"],
                    bubble_chamber.concepts["outer"],
                    bubble_chamber.concepts["forward"],
                    bubble_chamber.concepts["evaluate"],
                ]
            ]
        )
        return cls.spawn(parent_id, bubble_chamber, target_structures, urgency)

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
