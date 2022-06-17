from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.builder import Builder
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures import Frame


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
        self.frame = target_structures.get("frame")
        self.contextual_space = target_structures.get("contextual_space")
        self.input_spaces = target_structures.get("input_spaces")
        self.output_space = target_structures.get("output_space")
        self.conceptual_spaces_map = target_structures.get("conceptual_spaces_map")

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

    @property
    def targets_dict(self):
        return {
            "frame": self.frame,
            "contextual_space": self.contextual_space,
        }

    @property
    def target_structures(self) -> StructureCollection:
        return self.bubble_chamber.new_structure_collection(
            self.frame, self.contextual_space
        )

    def _passes_preliminary_checks(self):
        return True

    def _fizzle(self):
        pass

    def _instantiate_frame(self, frame: Frame) -> Frame:
        frame_instance = frame.copy(
            parent_id=self.codelet_id, bubble_chamber=self.bubble_chamber
        )
        self.bubble_chamber.frame_instances.add(frame_instance)
        self.bubble_chamber.loggers["structure"].log(frame_instance)
        return frame_instance
