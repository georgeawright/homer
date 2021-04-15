from homer.codelets.evaluators import ViewEvaluator
from homer.structures.views import SimplexView


class MonitoringViewEvaluator(ViewEvaluator):
    @classmethod
    def get_target_class(cls):
        return SimplexView
