from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.builders import ViewBuilder
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.location import Location
from linguoplotter.structures.spaces import ContextualSpace
from linguoplotter.structures.views import SimplexView


class SimplexViewBuilder(ViewBuilder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        ViewBuilder.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.frame = target_structures.get("frame")
        self.contextual_space = target_structures.get("contextual_space")
        self.conceptual_spaces_map = target_structures.get("conceptual_spaces_map")

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators.view_evaluators import (
            SimplexViewEvaluator,
        )

        return SimplexViewEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-simplex"]

    @property
    def targets_dict(self):
        return {
            "frame": self.frame,
            "contextual_space": self.contextual_space,
        }

    def _process_structure(self):
        view_id = ID.new(SimplexView)
        input_space_concept = self.contextual_space.parent_concept
        self.bubble_chamber.loggers["activity"].log_dict(
            self, self.conceptual_spaces_map, "Conceptual spaces map"
        )
        frame_input_space = (
            self.frame.input_space
            if self.frame.input_space.parent_concept == input_space_concept
            else self.frame.output_space
        )
        frame_instance = self.frame.instantiate(
            input_space=frame_input_space,
            conceptual_spaces_map=self.conceptual_spaces_map,
            parent_id=self.codelet_id,
            bubble_chamber=self.bubble_chamber,
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Created frame instance: {frame_instance}"
        )
        view_output = ContextualSpace(
            structure_id=ID.new(ContextualSpace),
            parent_id=self.codelet_id,
            name=f"output for {view_id}",
            parent_concept=frame_instance.output_space.parent_concept,
            contents=self.bubble_chamber.new_structure_collection(),
            conceptual_spaces=frame_instance.output_space.conceptual_spaces,
            links_in=self.bubble_chamber.new_structure_collection(),
            links_out=self.bubble_chamber.new_structure_collection(),
            parent_spaces=self.bubble_chamber.new_structure_collection(),
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Created output space: {view_output}"
        )
        view = SimplexView(
            structure_id=view_id,
            parent_id=self.codelet_id,
            parent_frame=frame_instance,
            locations=[Location([], self.bubble_chamber.spaces["views"])],
            members=self.bubble_chamber.new_structure_collection(),
            frames=self.bubble_chamber.new_structure_collection(frame_instance),
            input_spaces=self.bubble_chamber.new_structure_collection(
                self.contextual_space
            ),
            output_space=view_output,
            quality=0,
            links_in=self.bubble_chamber.new_structure_collection(),
            links_out=self.bubble_chamber.new_structure_collection(),
            parent_spaces=self.bubble_chamber.new_structure_collection(),
            sub_views=self.bubble_chamber.new_structure_collection(),
            super_views=self.bubble_chamber.new_structure_collection(),
        )
        self.bubble_chamber.loggers["structure"].log(view_output)
        self.bubble_chamber.contextual_spaces.add(view_output)
        self.bubble_chamber.loggers["structure"].log(view)
        self.bubble_chamber.views.add(view)
        self.bubble_chamber.loggers["structure"].log_view(view)
        self._structure_concept.instances.add(view)
        self._structure_concept.recalculate_exigency()
        self.child_structures = self.bubble_chamber.new_structure_collection(view)
