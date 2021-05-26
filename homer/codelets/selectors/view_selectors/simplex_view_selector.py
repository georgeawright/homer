from homer.bubble_chamber import BubbleChamber
from homer.codelets.selectors import ViewSelector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structures.views import SimplexView


class SimplexViewSelector(ViewSelector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        champion = bubble_chamber.simplex_views.get_active()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({champion}),
            champion.activation,
        )

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
            champion_view = self.champions.get_random()
            challenger_view = champion_view.nearby().get_random()
            self.challengers = StructureCollection({challenger_view})
        except MissingStructureError:
            return True
        champion_members_starts = StructureCollection(
            {
                member.start
                for member in champion_view.members
                if member.start.parent_space.parent_concept.name == "input"
            }
        )
        return not StructureCollection(
            {
                member.start
                for member in challenger_view.members
                if member.start.parent_space.parent_concept.name == "input"
                and member.start in champion_members_starts
            }
        ).is_empty()
