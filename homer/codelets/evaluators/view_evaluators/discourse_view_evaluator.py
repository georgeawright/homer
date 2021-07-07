import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import ViewEvaluator
from homer.structure_collection import StructureCollection


class DiscourseViewEvaluator(ViewEvaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["view-discourse"]
        target = bubble_chamber.monitoring_views.get()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({target}),
            structure_type.activation,
        )

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors.view_selectors import DiscourseViewSelector

        return DiscourseViewSelector

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["view-discourse"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_view = self.target_structures.get()
        proportion_of_slots_filled = len(target_view.slot_values) / len(
            target_view.slots
        )
        average_correspondence_quality = (
            statistics.fmean([member.quality for member in target_view.members])
            if len(target_view.members) > 0
            else 0
        )
        self.confidence = statistics.fmean(
            [proportion_of_slots_filled, average_correspondence_quality]
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
