import statistics

from homer.codelets.evaluators import ViewEvaluator


class SimplexViewEvaluator(ViewEvaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors.view_selectors import SimplexViewSelector

        return SimplexViewSelector

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["view-simplex"]
        return structure_concept.relations_with(self._evaluate_concept).get_random()

    def _calculate_confidence(self):
        target_view = self.target_structures.get_random()
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
