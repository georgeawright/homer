from homer.bubble_chamber import BubbleChamber
from homer.codelets.selectors import ViewSelector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structures.views import DiscourseView


class DiscourseViewSelector(ViewSelector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        champion = bubble_chamber.discourse_views.get_active()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({champion}),
            champion.activation,
        )

    @classmethod
    def get_target_class(cls):
        return DiscourseView

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-discourse"]
