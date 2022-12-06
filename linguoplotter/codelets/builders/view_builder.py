from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.builder import Builder
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.location import Location
from linguoplotter.structure_collections import StructureDict
from linguoplotter.structures import View
from linguoplotter.structures.spaces import ContextualSpace


class ViewBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators import ViewEvaluator

        return ViewEvaluator

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
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        return True

    def _process_structure(self):
        view_id = ID.new(View)
        input_space_concept = self.targets["contextual_space"].parent_concept
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
        view_output = ContextualSpace(
            structure_id=ID.new(ContextualSpace),
            parent_id=self.codelet_id,
            name=f"output for {view_id}",
            parent_concept=frame_instance.output_space.parent_concept,
            contents=self.bubble_chamber.new_set(),
            conceptual_spaces=frame_instance.output_space.conceptual_spaces,
            links_in=self.bubble_chamber.new_set(),
            links_out=self.bubble_chamber.new_set(),
            parent_spaces=self.bubble_chamber.new_set(),
            champion_labels=self.bubble_chamber.new_set(),
            champion_relations=self.bubble_chamber.new_set(),
        )
        self.bubble_chamber.loggers["activity"].log(
            f"Created output space: {view_output}"
        )
        view = View(
            structure_id=view_id,
            parent_id=self.codelet_id,
            parent_frame=frame_instance,
            locations=[Location([], self.bubble_chamber.spaces["views"])],
            members=self.bubble_chamber.new_set(),
            frames=self.bubble_chamber.new_set(frame_instance),
            input_spaces=self.bubble_chamber.new_set(self.targets["contextual_space"]),
            output_space=view_output,
            quality=0,
            links_in=self.bubble_chamber.new_set(),
            links_out=self.bubble_chamber.new_set(),
            parent_spaces=self.bubble_chamber.new_set(),
            sub_views=self.bubble_chamber.new_set(),
            super_views=self.bubble_chamber.new_set(),
            champion_labels=self.bubble_chamber.new_set(),
            champion_relations=self.bubble_chamber.new_set(),
        )
        frame_instance.progenitor.instances.add(view)
        frame_instance.parent_concept.instances.add(view)
        self.bubble_chamber.loggers["structure"].log(view_output)
        self.bubble_chamber.contextual_spaces.add(view_output)
        self.bubble_chamber.loggers["structure"].log(view)
        self.bubble_chamber.views.add(view)
        self.bubble_chamber.loggers["structure"].log_view(view)
        self._structure_concept.instances.add(view)
        self._structure_concept.recalculate_exigency()
        self.child_structures.add(view)

    def _fizzle(self):
        pass
