import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import ViewSuggester
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation


class DiscourseViewSuggester(ViewSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.view_builders import DiscourseViewBuilder

        return DiscourseViewBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        monitoring_view_one = bubble_chamber.monitoring_views.get(key=activation)
        monitoring_view_two = bubble_chamber.monitoring_views.get(
            key=activation, exclude=[monitoring_view_one]
        )
        text_space_one = monitoring_view_one.output_space
        text_space_two = monitoring_view_two.output_space
        frame = bubble_chamber.frames.where(
            parent_concept=bubble_chamber.concepts["discourse"]
        ).get(key=activation)
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
