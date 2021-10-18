import statistics

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import ViewEvaluator


class MonitoringViewEvaluator(ViewEvaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["view-monitoring"]
        target = bubble_chamber.monitoring_views.get()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            bubble_chamber.new_structure_collection(target),
            structure_type.activation,
        )

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors.view_selectors import MonitoringViewSelector

        return MonitoringViewSelector

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["view-monitoring"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_view = self.target_structures.get()
        original_input_space = self.bubble_chamber.spaces["input"]
        size_of_input_space = sum(
            1 for chunk in original_input_space.contents.where(is_raw=True)
        ) * len(original_input_space.conceptual_spaces)
        raw_inputs_in_interpretation = {
            space: set() for space in original_input_space.conceptual_spaces
        }
        for member in target_view.members:
            for argument in member.end.arguments:
                for raw_member in argument.raw_members:
                    raw_inputs_in_interpretation[member.conceptual_space].add(
                        raw_member
                    )
        no_of_raw_inputs_in_interpretation = sum(
            len(raw_input_set)
            for raw_input_set in raw_inputs_in_interpretation.values()
        )
        proportion_of_raw_inputs_in_interpretation = (
            no_of_raw_inputs_in_interpretation / size_of_input_space
        )
        average_correspondence_quality = (
            statistics.fmean([member.quality for member in target_view.members])
            if len(target_view.members) > 0
            else 0
        )
        # should take into account no of interpretations of text
        self.confidence = fuzzy.AND(
            statistics.fmean(
                [
                    proportion_of_raw_inputs_in_interpretation,
                    average_correspondence_quality,
                ]
            ),
            target_view.output_space.quality,
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
