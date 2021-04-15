import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Evaluator
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structures.nodes import Phrase


class PhraseEvaluator(Evaluator):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structure: Structure,
        urgency: FloatBetweenOneAndZero,
    ):
        Evaluator.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structure, urgency
        )
        self.original_confidence = self.target_structure.quality

    @classmethod
    def get_target_class(cls):
        return Phrase

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structure: Structure,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, target_structure, urgency)

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["phrase"]
        target = bubble_chamber.phrases.get_random()
        return cls.spawn(parent_id, bubble_chamber, target, structure_type.activation)

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["phrase"]
        return structure_concept.relations_with(self._evaluate_concept).get_random()

    def _calculate_confidence(self):
        left_branch_quality = (
            self.target_structure.left_branch.quality
            if isinstance(self.target_structure.left_branch, Phrase)
            else self.target_structure.left_branch.label_of_type(
                self.target_structure.rule.left_branch
            ).quality
        )
        right_branch_quality = (
            self.target_structure.right_branch.quality
            if isinstance(self.target_structure.right_branch, Phrase)
            else self.target_structure.right_branch.label_of_type(
                self.target_structure.rule.right_branch
            ).quality
        )
        self.confidence = statistics.fmean(
            [
                left_branch_quality,
                right_branch_quality,
                self.target_structure.rule.activation,
                self.target_structure.unchunkedness,
                self.target_structure.size,
            ]
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
