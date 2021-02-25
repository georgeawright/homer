from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator
from homer.codelets.selectors import LabelSelector
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures.links import Label
from homer.structures.nodes import Word


class WordEvaluator(Evaluator):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structure: Word,
        urgency: FloatBetweenOneAndZero,
    ):
        Evaluator.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structure, urgency
        )
        self.original_confidence = self.target_structure.quality

    @classmethod
    def get_target_class(cls):
        return Word

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structure: Word,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, target_structure, urgency)

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["word"]
        target = bubble_chamber.words.get_random()
        return cls.spawn(parent_id, bubble_chamber, target, structure_type.activation)

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["word"]
        return structure_concept.relations_with(self._evaluate_concept).get_random()

    def _calculate_confidence(self):
        if self.target_structure.concepts is None:
            self.confidence = 1.0
        else:
            labels = StructureCollection.union(
                *[
                    correspondee.labels
                    for correspondee in self.target_structure.correspondees
                ]
            )
            compatible_labels = [
                label
                for label in labels
                if label.parent_concept in self.target_structure.concepts
            ]
            self.confidence = max(label.quality for label in compatible_labels)
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
