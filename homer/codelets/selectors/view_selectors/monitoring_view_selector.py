from homer.codelets.selectors import ViewSelector
from homer.structures.views import MonitoringView


class MonitoringViewSelector(ViewSelector):
    @classmethod
    def get_target_class(cls):
        return MonitoringView
