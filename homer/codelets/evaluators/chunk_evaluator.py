import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator
from homer.codelets.selectors import ChunkSelector
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structure_collection import StructureCollection


class ChunkEvaluator(Evaluator):
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
        structure_type = bubble_chamber.concepts["chunk"]
        target = bubble_chamber.chunks.get_random()
        return cls.spawn(parent_id, bubble_chamber, target, structure_type.activation)

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["chunk"]
        return structure_concept.relations_with(self._evaluate_concept).get_random()

    def _calculate_confidence(self):
        proximities = [
            space.proximity_between(member, self.target_structure)
            for space in self.target_structure.parent_spaces
            for member in self.target_structure.members
            if space.is_basic_level
        ]
        self.confidence = statistics.fmean(proximities) if proximities != [] else 0
        self.change_in_confidence = abs(self.confidence - self.original_confidence)

    def _engender_follow_up(self):
        target_space = StructureCollection(
            {
                space
                for space in self.target_structure.parent_spaces
                if space.is_basic_level
            }
        ).get_random()
        self.child_codelets.append(
            ChunkSelector.spawn(
                self.codelet_id,
                self.bubble_chamber,
                target_space,
                self.target_structure,
                self.change_in_confidence,
            )
        )
