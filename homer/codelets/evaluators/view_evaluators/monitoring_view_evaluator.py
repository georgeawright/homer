import statistics

from homer.codelets.evaluators import ViewEvaluator
from homer.structures.views import MonitoringView


class MonitoringViewEvaluator(ViewEvaluator):
    @classmethod
    def get_target_class(cls):
        return MonitoringView

    def _calculate_confidence(self):
        raw_input_size = sum(
            1 for item in self.target_structure.raw_input_space.contents if item.is_raw
        )
        amount_of_raw_input_in_interpretation = sum(
            1
            for correspondence in self.target_structure.members
            if correspondence.start in self.target_structure.raw_input_space.contents
            or correspondence.end in self.target_structure.raw_input_space.contents
        )
        proportion_of_raw_input_in_interpretation = (
            amount_of_raw_input_in_interpretation / raw_input_size
        )
        average_correspondence_quality = (
            statistics.fmean(
                [member.quality for member in self.target_structure.members]
            )
            if len(self.target_structure.members) > 0
            else 0
        )
        self.confidence = statistics.fmean(
            [proportion_of_raw_input_in_interpretation, average_correspondence_quality]
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
