from homer.codelets.selectors import ViewSelector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structures.views import DiscourseView


class DiscourseViewSelector(ViewSelector):
    @classmethod
    def get_target_class(cls):
        return DiscourseView

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-discourse"]
