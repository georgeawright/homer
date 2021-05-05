import statistics

from homer.codelets.evaluators import ViewEvaluator
from homer.structures.nodes import Chunk


class MonitoringViewEvaluator(ViewEvaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors.view_selectors import MonitoringViewSelector

        return MonitoringViewSelector

    def _calculate_confidence(self):
        target_view = self.target_structures.get_random()
        chunks_in_interpretation = target_view.interpretation_space.contents.of_type(
            Chunk
        )
        no_of_chunks_with_correspondences_to_raw_input = sum(
            1 for chunk in chunks_in_interpretation if not chunk.members.is_empty()
        )
        proportion_of_interpretation_corresponding_to_raw_input = (
            (
                no_of_chunks_with_correspondences_to_raw_input
                / len(chunks_in_interpretation)
            )
            if len(chunks_in_interpretation) != 0
            else 0
        )
        average_correspondence_quality = (
            statistics.fmean([member.quality for member in target_view.members])
            if len(target_view.members) > 0
            else 0
        )
        no_of_monitoring_views_with_text_input = len(
            self.bubble_chamber.monitoring_views.where(
                text_space=target_view.text_space
            )
        )
        self.confidence = (
            statistics.fmean(
                [
                    proportion_of_interpretation_corresponding_to_raw_input,
                    average_correspondence_quality,
                ]
            )
            / no_of_monitoring_views_with_text_input
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
