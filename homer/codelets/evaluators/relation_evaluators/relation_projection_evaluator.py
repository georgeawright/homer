from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import RelationEvaluator
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence


class RelationProjectionEvaluator(RelationEvaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        raise NotImplementedError

    def _calculate_confidence(self):
        target_correspondence = self.target_structures.where(
            is_correspondence=True
        ).get_random()
        self.confidence = target_correspondence.start.quality
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
