from homer.codelets.builders import ViewBuilder
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.spaces import Frame, WorkingSpace
from homer.structures.views import MonitoringView


class MonitoringViewBuilder(ViewBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.view_evaluators import MonitoringViewEvaluator

        return MonitoringViewEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-monitoring"]

    def _passes_preliminary_checks(self):
        for view in self.bubble_chamber.views:
            if (
                StructureCollection.intersection(view.input_spaces, self.target_spaces)
                == self.target_spaces
            ):
                return False
        if self.frame is None:
            for space in self.target_spaces:
                if isinstance(space, Frame):
                    self.frame = space
        return True

    def _process_structure(self):
        view_id = ID.new(MonitoringView)
        view_location = Location([], self.bubble_chamber.spaces["top level working"])
        view_output = self.target_spaces.get()
        interpretation_space = WorkingSpace(
            structure_id=ID.new(WorkingSpace),
            parent_id=self.codelet_id,
            name=f"interpretation for {view_id}",
            parent_concept=self.bubble_chamber.concepts["interpretation"],
            conceptual_space=None,
            locations=[view_location],
            contents=StructureCollection(),
            no_of_dimensions=0,
            dimensions=[],
            sub_spaces=[],
        )
        self.target_spaces.add(interpretation_space)
        view = MonitoringView(
            structure_id=view_id,
            parent_id=self.codelet_id,
            location=view_location,
            members=StructureCollection(),
            input_spaces=self.target_spaces,
            output_space=view_output,
            quality=0,
        )
        self.bubble_chamber.logger.log(interpretation_space)
        self.bubble_chamber.logger.log(view)
        self.bubble_chamber.views.add(view)
        self.child_structures = StructureCollection({view})
