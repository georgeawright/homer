import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ViewBuilder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
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

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        monitoring_view_one = bubble_chamber.monitoring_views.get_active()
        monitoring_view_two = bubble_chamber.monitoring_views.get_active(
            exclude=[monitoring_view_one]
        )
        text_space_one = monitoring_view_one.output_space
        text_space_two = monitoring_view_two.output_space
        frame = bubble_chamber.frames.where(
            parent_concept=bubble_chamber.concepts["discourse"]
        ).get_active()
        targets = StructureCollection({text_space_one, text_space_two, frame})
        urgency = (
            urgency
            if urgency is not None
            else statistics.fmean([space.activation for space in targets])
        )
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-discourse"]

    def _process_structure(self):
        view_id = ID.new(DiscourseView)
        view_location = Location([], self.bubble_chamber.spaces["top level working"])
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
            input_spaces=self.target_spaces,
            output_space=view_output,
            quality=0,
        )
        self.bubble_chamber.logger.log(view_output)
        self.bubble_chamber.logger.log(view)
        self.bubble_chamber.views.add(view)
        self.child_structures = StructureCollection({view})
