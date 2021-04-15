from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ViewBuilder
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.spaces import WorkingSpace
from homer.structures.views import MonitoringView


class MonitoringViewBuilder(ViewBuilder):
    @classmethod
    def get_target_class(cls):
        return MonitoringView

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber, urgency: float = None):
        raise NotImplementedError

    def _process_structure(self):
        raise NotImplementedError
