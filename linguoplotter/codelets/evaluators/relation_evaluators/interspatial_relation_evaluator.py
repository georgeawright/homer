from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import RelationEvaluator
from linguoplotter.hyper_parameters import HyperParameters


class InterspatialRelationEvaluator(RelationEvaluator):
    FLOATING_POINT_TOLERANCE = HyperParameters.FLOATING_POINT_TOLERANCE

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors.relation_selectors import (
            InterspatialRelationSelector,
        )

        return InterspatialRelationSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        view = bubble_chamber.views.filter(
            lambda x: x.unhappiness < cls.FLOATING_POINT_TOLERANCE
            and x.parent_frame.parent_concept.location_in_space(
                bubble_chamber.spaces["grammar"]
            )
            == bubble_chamber.concepts["sentence"].location_in_space(
                bubble_chamber.spaces["grammar"]
            )
        ).get()
        target = view.output_space.contents.filter(
            lambda x: x.is_interspatial and x.is_relation
        ).get(key=lambda x: abs(x.activation - x.quality))
        targets = bubble_chamber.new_set(target, name="targets")
        return cls.spawn(
            parent_id,
            bubble_chamber,
            targets,
            abs(target.activation - target.quality),
        )

    def _calculate_confidence(self):
        target_relation = self.targets.get()
        minimum_space_quality = min(
            target_relation.start.parent_space.quality,
            target_relation.end.parent_space.quality,
        )
        classification = target_relation.parent_concept.classifier.classify(
            space=target_relation.conceptual_space,
            concept=target_relation.parent_concept,
            start=target_relation.start
            if not target_relation.start.is_slot
            else target_relation.start.non_slot_value,
            end=target_relation.end
            if not target_relation.end.is_slot
            else target_relation.end.non_slot_value,
        )
        target_relation.quality = classification * minimum_space_quality
        self.confidence = target_relation.quality
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_relation.activation
