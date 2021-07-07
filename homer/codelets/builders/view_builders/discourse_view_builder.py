from homer.codelets.builders import ViewBuilder
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.spaces import WorkingSpace
from homer.structures.views import DiscourseView


class DiscourseViewBuilder(ViewBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.view_evaluators import DiscourseViewEvaluator

        return DiscourseViewEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-discourse"]

    def _passes_preliminary_checks(self):
        for view in self.bubble_chamber.views:
            if all(
                [
                    input_space in self.target_spaces
                    or any(
                        [
                            input_space.has_relation_with(target_space)
                            for target_space in self.target_spaces
                        ]
                    )
                    for input_space in view.input_spaces
                ]
            ):
                return False
        if self.frame is None:
            for space in self.target_spaces:
                if space.is_frame:
                    self.frame = space
        return True

    def _process_structure(self):
        view_id = ID.new(DiscourseView)
        view_location = Location([], self.bubble_chamber.spaces["top level working"])
        input_spaces = StructureCollection(
            {
                self._instantiate_frame(space) if space.is_frame else space
                for space in self.target_spaces
            }
        )
        view_output = WorkingSpace(
            structure_id=ID.new(WorkingSpace),
            parent_id=self.codelet_id,
            name=f"output for {view_id}",
            parent_concept=self.frame.parent_concept,
            conceptual_space=self.frame.conceptual_space,
            locations=[view_location],
            contents=StructureCollection(),
            no_of_dimensions=1,
            dimensions=[],
            sub_spaces=[],
        )
        view = DiscourseView(
            structure_id=view_id,
            parent_id=self.codelet_id,
            location=view_location,
            members=StructureCollection(),
            input_spaces=input_spaces,
            output_space=view_output,
            quality=0,
        )
        self.bubble_chamber.logger.log(view_output)
        self.bubble_chamber.logger.log(view)
        self.bubble_chamber.views.add(view)
        self.child_structures = StructureCollection({view})
