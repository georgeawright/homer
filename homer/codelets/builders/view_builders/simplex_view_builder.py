from homer.codelets.builders import ViewBuilder
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.spaces import ContextualSpace
from homer.structures.views import SimplexView


class SimplexViewBuilder(ViewBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator

        return SimplexViewEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-simplex"]

    def _process_structure(self):
        view_id = ID.new(SimplexView)
        view_location = Location([], self.bubble_chamber.spaces["top level working"])
        frame = self.target_spaces.where(is_frame=True).get()
        input_space_concept = (
            self.target_spaces.where(is_frame=False).get().parent_concept
        )
        frame_input_space = (
            frame.input_space
            if frame.input_space.parent_concept == input_space_concept
            else frame.output_space
        )
        frame_instance = frame.instantiate(
            input_space=frame_input_space,
            parent_id=self.codelet_id,
            bubble_chamber=self.bubble_chamber,
        )
        input_spaces = StructureCollection.union(
            self.target_spaces.where(is_frame=False),
            StructureCollection({frame_instance}),
        )
        view_output = ContextualSpace(
            structure_id=ID.new(ContextualSpace),
            parent_id=self.codelet_id,
            name=f"output for {view_id}",
            parent_concept=self.frame.output_space.parent_concept,
            contents=StructureCollection(),
            conceptual_spaces=self.frame.output_space.conceptual_spaces,
        )
        view = SimplexView(
            structure_id=view_id,
            parent_id=self.codelet_id,
            location=view_location,
            members=StructureCollection(),
            input_spaces=input_spaces,
            output_space=view_output,
            quality=0,
        )
        self.bubble_chamber.logger.log(view_output)
        self.bubble_chamber.working_spaces.add(view_output)
        self.bubble_chamber.logger.log(view)
        self.bubble_chamber.views.add(view)
        self.child_structures = StructureCollection({view})
