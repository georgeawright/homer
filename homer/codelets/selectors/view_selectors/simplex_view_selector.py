from homer.codelets.selectors import ViewSelector
from homer.errors import MissingStructureError
from homer.structures.views import SimplexView


class SimplexViewSelector(ViewSelector):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.suggesters.view_suggesters import SimplexViewSuggester

        return SimplexViewSuggester

    @classmethod
    def get_target_class(cls):
        return SimplexView

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-simplex"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            champion_view = self.champions.get()
            challenger_view = champion_view.nearby().get()
            self.challengers = self.bubble_chamber.new_structure_collection(
                challenger_view
            )
        except MissingStructureError:
            return True
        champion_members_starts = self.bubble_chamber.new_structure_collection(
            member.start
            for member in champion_view.members
            if member.start.parent_space.parent_concept.name == "input"
        )
        return not self.bubble_chamber.new_structure_collection(
            member.start
            for member in challenger_view.members
            if member.start.parent_space.parent_concept.name == "input"
            and member.start in champion_members_starts
        ).is_empty()
