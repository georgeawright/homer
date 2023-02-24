from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.builder import Builder
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict


class FrameBuilder(Builder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators import FrameEvaluator

        return FrameEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["frame"]

    def _passes_preliminary_checks(self):
        return not any(
            [
                frame.is_equivalent_to(self.targets["frame"])
                for frame in self.targets["view"].secondary_frames
            ]
        )

    def _process_structure(self):
        input_space_concept = self.targets[
            "view"
        ].parent_frame.input_space.parent_concept
        frame_input_space = (
            self.targets["frame"].input_space
            if self.targets["frame"].input_space.parent_concept == input_space_concept
            else self.targets["frame"].output_space
        )
        space_map = (
            {} if self.targets["space_map"] is None else self.targets["space_map"]
        )
        frame_instance = self.targets["frame"].instantiate(
            input_space=frame_input_space,
            conceptual_spaces_map=space_map,
            parent_id=self.codelet_id,
            bubble_chamber=self.bubble_chamber,
        )
        self.bubble_chamber.loggers["activity"].log(
            f"Created frame instance: {frame_instance}"
        )
        self.targets["view"].secondary_frames.add(frame_instance)
        frame_instance.parent_view = self.targets["view"]
        frame_instance.progenitor.instances.add(self.targets["view"])
        frame_instance.parent_concept.instances.add(self.targets["view"])
        self.bubble_chamber.loggers["structure"].log(self.targets["view"])
        self.child_structures.add(frame_instance)

    def _fizzle(self):
        pass
