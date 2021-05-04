import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Evaluator
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Phrase


class PhraseEvaluator(Evaluator):
    @classmethod
    def get_target_class(cls):
        return Phrase

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["phrase"]
        target = bubble_chamber.phrases.get_random()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({target}),
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["phrase"]
        return structure_concept.relations_with(self._evaluate_concept).get_random()

    def _calculate_confidence(self):
        target_phrase = self.target_structures.get_random()
        left_branch_quality = (
            target_phrase.left_branch.quality
            if isinstance(target_phrase.left_branch, Phrase)
            else target_phrase.left_branch.label_of_type(
                target_phrase.rule.left_branch
            ).quality
        )
        right_branch_quality = (
            target_phrase.right_branch.quality
            if isinstance(target_phrase.right_branch, Phrase)
            else target_phrase.right_branch.label_of_type(
                target_phrase.rule.right_branch
            ).quality
        )
        self.confidence = statistics.fmean(
            [
                left_branch_quality,
                right_branch_quality,
                target_phrase.rule.activation,
                target_phrase.unchunkedness,
                target_phrase.size,
            ]
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
