from linguoplotter.codelets.selectors import ViewSelector
from linguoplotter.structures.views import DiscourseView


class DiscourseViewSelector(ViewSelector):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.suggesters.view_suggesters import (
            DiscourseViewSuggester,
        )

        return DiscourseViewSuggester

    @classmethod
    def get_target_class(cls):
        return DiscourseView

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-discourse"]
