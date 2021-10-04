from homer.codelets.selectors import ViewSelector
from homer.codelets.suggesters.view_suggesters import MonitoringViewSuggester
from homer.structures.views import MonitoringView


class MonitoringViewSelector(ViewSelector):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.suggesters.view_suggesters import MonitoringViewSuggester

        return MonitoringViewSuggester

    @classmethod
    def get_target_class(cls):
        return MonitoringView

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-monitoring"]

    def _engender_follow_up(self):
        winning_view = self.winners.get()
        input_spaces = winning_view.input_spaces
        output_space = winning_view.output_space
        self.child_codelets = [
            MonitoringViewSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {
                    "input_spaces": input_spaces,
                    "output_space": output_space,
                },
                winning_view.activation,
            ),
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            ),
        ]
