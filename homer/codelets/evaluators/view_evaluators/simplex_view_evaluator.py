import statistics

from homer.codelets.evaluators import ViewEvaluator
from homer.structures.views import SimplexView


class SimplexViewEvaluator(ViewEvaluator):
    @classmethod
    def get_target_class(cls):
        return SimplexView

    def _calculate_confidence(self):
        proportion_of_slots_filled = len(self.target_structure.slot_values) / len(
            self.target_structure.slots
        )
        average_correspondence_quality = (
            statistics.fmean(
                [member.quality for member in self.target_structure.members]
            )
            if len(self.target_structure.members) > 0
            else 0
        )
        self.confidence = statistics.fmean(
            [proportion_of_slots_filled, average_correspondence_quality]
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
