from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures.spaces import Frame


class ViewBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self._target_structures = target_structures
        self._input_spaces = None
        self._ouptut_space = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_spaces: StructureCollection,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_spaces,
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def target_structures(self):
        return StructureCollection(self._target_structures)

    def _passes_preliminary_checks(self):
        self.frame = self._target_structures["frame"]
        self.contextual_space = self._target_structures["contextual_space"]
        return True

    def _fizzle(self):
        pass

    def _instantiate_frame(self, frame: Frame) -> Frame:
        frame_instance = frame.copy(
            parent_id=self.codelet_id, bubble_chamber=self.bubble_chamber
        )
        self.bubble_chamber.frame_instances.add(frame_instance)
        self.bubble_chamber.logger.log(frame_instance)
        return frame_instance
