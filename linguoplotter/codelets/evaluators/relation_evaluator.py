from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluator import Evaluator
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collections import StructureSet


class RelationEvaluator(Evaluator):
    CLASSIFICATION_WEIGHT = HyperParameters.RELATION_QUALITY_CLASSIFICATION_WEIGHT
    SAMENESS_WEIGHT = HyperParameters.RELATION_QUALITY_SAMENESS_WEIGHT

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors import RelationSelector

        return RelationSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        input_space = bubble_chamber.input_spaces.get()
        target = input_space.contents.where(is_relation=True).get(
            key=lambda x: abs(x.activation - x.quality)
        )
        targets = bubble_chamber.new_set(target, name="targets")
        return cls.spawn(
            parent_id,
            bubble_chamber,
            targets,
            abs(target.activation - target.quality),
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["relation"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_relation = self.targets.get()
        minimum_argument_quality = min(
            target_relation.start.quality, target_relation.end.quality
        )
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
                start=relation.start,
                end=relation.end,
            )
            * minimum_argument_quality
            / relation.parent_concept.number_of_components
            for relation in parallel_relations
        }
        sameness_confidence = max(
            classification
            if relation.parent_concept == self.bubble_chamber.concepts["same"]
            else 0
            for relation, classification in classifications.items()
        )
        # TODO: maybe also have different time relation confidence?
        for relation in classifications:
            relation.quality = sum(
                [
                    classifications[relation] * self.CLASSIFICATION_WEIGHT,
                    sameness_confidence * self.SAMENESS_WEIGHT,
                ]
            )
        self.confidence = target_relation.quality
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_relation.activation
