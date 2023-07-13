from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluator import Evaluator
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collections import StructureSet


class RelationEvaluator(Evaluator):
    CLASSIFICATION_WEIGHT = HyperParameters.RELATION_QUALITY_CLASSIFICATION_WEIGHT
    SAMENESS_WEIGHT = HyperParameters.RELATION_QUALITY_SAMENESS_WEIGHT
    TIME_WEIGHT = HyperParameters.RELATION_QUALITY_TIME_WEIGHT

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
        start_time = target_relation.start.location_in_space(
            self.bubble_chamber.spaces["time"]
        ).coordinates[0][0]
        end_time = target_relation.end.location_in_space(
            self.bubble_chamber.spaces["time"]
        ).coordinates[0][0]
        time_diff = abs(start_time - end_time)
        times_are_adjacent = 1 if time_diff <= 24 else 0.0
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
                start=relation.start
                if not relation.start.is_slot
                else relation.start.non_slot_value,
                end=relation.end
                if not relation.end.is_slot
                else relation.end.non_slot_value,
            )
            * minimum_argument_quality
            / (
                1
                if not relation.parent_concept.is_compound_concept
                # concepts with 2 components are fine, but more is unwieldy
                else relation.parent_concept.number_of_components - 1
            )
            * times_are_adjacent
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
