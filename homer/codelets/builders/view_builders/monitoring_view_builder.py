from homer.codelets.builders import ViewBuilder
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
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
        self.input_spaces = self._target_structures["input_spaces"]
        self.output_space = self._target_structures["output_space"]
        return True

    def _process_structure(self):
        view_id = ID.new(MonitoringView)
        view = MonitoringView(
            structure_id=view_id,
            parent_id=self.codelet_id,
            locations=[Location([], self.bubble_chamber.spaces["views"])],
            members=StructureCollection(),
            input_spaces=self.input_spaces,
            output_space=self.output_space,
            quality=0,
        )
        self.bubble_chamber.logger.log(view)
        self.bubble_chamber.views.add(view)
        self.child_structures = StructureCollection({view})
