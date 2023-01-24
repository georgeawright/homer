from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import RelationEvaluator
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collections import StructureSet


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
            and x.parent_frame.parent_concept == bubble_chamber.concepts["sentence"]
        ).get()
        target = view.output_space.contents.filter(
            lambda x: x.is_interspatial_relation
        ).get(key=lambda x: abs(x.activation - x.quality))
        targets = bubble_chamber.new_set(target, name="targets")
        return cls.spawn(
            parent_id,
            bubble_chamber,
            targets,
            abs(target.activation - target.quality),
        )

    def _calculate_confidence(self):
        # TODO
        target_relation = self.targets.get()
        start = (
            target_relation.start.non_slot_value
            if target_relation.start.is_slot
            else target_relation.start
        )
        end = (
            target_relation.end.non_slot_value
            if target_relation.end.is_slot
            else target_relation.end
        )
        if None in [start, end]:
            self.confidence = 0.0
            self.change_in_confidence = abs(self.confidence - self.original_confidence)
            self.activation_difference = self.confidence - target_relation.activation
            return
        minimum_argument_quality = min(start.quality, end.quality)
        parallel_relations = StructureSet.intersection(
            target_relation.start.relations, target_relation.end.relations
        )
        self.bubble_chamber.loggers["activity"].log_set(
            parallel_relations, "Parallel relations"
        )
        classifications = {
            relation: relation.parent_concept.classifier.classify(
                space=relation.conceptual_space,
                concept=relation.parent_concept,
                start=relation.start
                if not relation.start.is_slot
                else relation.start.non_slot_value,
                end=relation.end
                if not relation.end.is_slot
                else relation.end.non_slot_value,
            )
            * minimum_argument_quality
            / relation.parent_concept.number_of_components
            for relation in parallel_relations
        }
        sameness_classifications = {
            relation.conceptual_space: classification
            for relation, classification in classifications.items()
            if relation.parent_concept == self.bubble_chamber.concepts["same"]
        }
        sameness_confidence = 0
        sameness_relation_weight = 1
        for _, classification in sameness_classifications.items():
            sameness_relation_weight /= 2
            sameness_confidence += classification * sameness_relation_weight
        time_difference_confidence = 0
        for relation, classification in classifications.items():
            if (
                relation.conceptual_space == self.bubble_chamber.spaces["time"]
                and relation.parent_concept == self.bubble_chamber.concepts["less"]
            ):
                time_difference_confidence = classification
        for relation in classifications:
            relation.quality = sum(
                [
                    classifications[relation] * self.CLASSIFICATION_WEIGHT,
                    sameness_confidence * self.SAMENESS_WEIGHT,
                    time_difference_confidence * self.TIME_WEIGHT,
                ]
            )
        self.confidence = target_relation.quality
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_relation.activation
