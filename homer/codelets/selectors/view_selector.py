from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection


class ViewSelector(Selector):
    @classmethod
    def get_follow_up_class(cls) -> type:
        raise NotImplementedError

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            champion_view = self.champions.get()
            challenger_view = champion_view.nearby().get()
            self.challengers = StructureCollection({challenger_view})
        except MissingStructureError:
            return True
        return True

    def _engender_follow_up(self):
        self.child_codelets.append(
            self.get_follow_up_class().make(self.codelet_id, self.bubble_chamber)
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
                challengers=self.challengers,
            )
        )

    def _fizzle(self):
        pass
