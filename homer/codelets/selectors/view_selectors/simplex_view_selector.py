from homer.codelets.selectors import ViewSelector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structures.views import SimplexView


class SimplexViewSelector(ViewSelector):
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
        members_intersection = StructureCollection.intersection(
            champion_view.members, challenger_view.members
        )
        return (
            len(members_intersection) > 0.5 * champion_view.size
            and len(members_intersection) > 0.5 * challenger_view.size
        )
