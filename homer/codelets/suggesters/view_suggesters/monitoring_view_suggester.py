import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import ViewSuggester
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection_keys import activation


class MonitoringViewSuggester(ViewSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.view_builders import MonitoringViewBuilder

        return MonitoringViewBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        interpretation_view = bubble_chamber.simplex_views.filter(
            lambda x: x.output_space.parent_concept == bubble_chamber.concepts["input"]
        ).get(key=activation)
        text_space = interpretation_view.input_contextual_spaces.get()
        interpretation_space = interpretation_view.output_space
        input_space = bubble_chamber.spaces["input"]
        urgency = urgency if urgency is not None else interpretation_view.activation
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "input_spaces": bubble_chamber.new_structure_collection(
                    interpretation_space, input_space
                ),
                "output_space": text_space,
            },
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-monitoring"]

    @property
    def target_structures(self):
        return self.input_spaces

    def _passes_preliminary_checks(self):
        self.input_spaces = self._target_structures["input_spaces"]
        return True

    def _calculate_confidence(self):
        self.confidence = statistics.fmean(
            [space.activation for space in self.input_spaces]
        )
