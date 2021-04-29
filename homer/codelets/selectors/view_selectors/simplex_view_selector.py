from homer.codelets.selectors import ViewSelector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structures.views import SimplexView


class SimplexViewSelector(ViewSelector):
    @classmethod
    def get_target_class(cls):
        return SimplexView

    def _passes_preliminary_checks(self):
        if self.challenger is not None:
            return True
        try:
            self.challenger = self.champion.nearby().get_random()
        except MissingStructureError:
            return True
        members_intersection = StructureCollection.intersection(
            self.champion.members, self.challenger.members
        )
        return len(members_intersection) > 0.5 * len(self.champion.members) and len(
            members_intersection
        ) > 0.5 * len(self.challenger.members)
