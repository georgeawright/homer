from linguoplotter.codelets.selectors import ViewSelector
from linguoplotter.structures.views import MonitoringView


class MonitoringViewSelector(ViewSelector):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.suggesters.view_suggesters import (
            MonitoringViewSuggester,
        )

        return MonitoringViewSuggester

    @classmethod
    def get_follow_up_evaluator(cls) -> type:
        from linguoplotter.codelets.evaluators.view_evaluators import (
            MonitoringViewEvaluator,
        )

        return MonitoringViewEvaluator

    @classmethod
    def get_target_class(cls):
        return MonitoringView

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-monitoring"]
