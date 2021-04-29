from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ViewBuilder
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.spaces import WorkingSpace
from homer.structures.views import MonitoringView


class MonitoringViewBuilder(ViewBuilder):
    @classmethod
    def get_target_class(cls):
        return MonitoringView

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber, urgency: float = None):
        target = StructureCollection(
            {
                space
                for space in bubble_chamber.working_spaces
                if space.parent_concept == bubble_chamber.concepts["text"]
                and not space.contents.is_empty()
            }
        ).get_exigent()
        urgency = urgency if urgency is not None else target.exigency
        return cls.spawn(
            parent_id, bubble_chamber, StructureCollection({target}), urgency
        )

    def _process_structure(self):
        view_id = ID.new(MonitoringView)
        view_location = Location([], self.bubble_chamber.spaces["top level working"])
        view_output = self.target_spaces.get_random()
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
        self.child_structure = view
