from homer.structures import View


class MonitoringView(View):
    @classmethod
    def get_builder_class(cls):
        from homer.codelets.builders.view_builders import MonitoringViewBuilder

        return MonitoringViewBuilder

    @classmethod
    def get_evaluator_class(cls):
        from homer.codelets.evaluators.view_evaluators import MonitoringViewEvaluator

        return MonitoringViewEvaluator

    @classmethod
    def get_selector_class(cls):
        from homer.codelets.selectors.view_selectors import MonitoringViewSelector

        return MonitoringViewSelector
