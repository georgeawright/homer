from linguoplotter import fuzzy
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
        parallel_relations = StructureSet.intersection(
            target_relation.start.parent_space.contents.filter(
                lambda x: x.is_relation
                and x.start.parent_space == target_relation.start.parent_space
                and x.parent_concept
                == target_relation.parent_concept  # TODO: or negation of opposite
                and x.conceptual_space == target_relation.conceptual_space
            ),
            target_relation.end.parent_space.contents.filter(
                lambda x: x.is_relation
                and x.end.parent_space == target_relation.end.parent_space
                and x.parent_concept == target_relation.parent_concept
                and x.conceptual_space == target_relation.conceptual_space
            ),
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
            * minimum_space_quality
            / relation.parent_concept.number_of_components
            for relation in parallel_relations
        }
        overall_classification = fuzzy.OR(
            *[classification for _, classification in classifications.items()]
        )
        for relation in classifications:
            relation.quality = sum(
                [
                    classifications[relation] * self.CLASSIFICATION_WEIGHT,
                    overall_classification * 1 - self.CLASSIFICATION_WEIGHT,
                ]
            )
        self.confidence = target_relation.quality
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_relation.activation
