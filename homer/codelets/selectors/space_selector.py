from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.structure_collection_keys import activation


class SpaceSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["conceptual-space"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        champion_space = self.champions.get()
        candidates = champion_space.nearby()
        try:
            challenger_space = candidates.get(key=activation, exclude=[champion_space])
            self.challengers = self.bubble_chamber.new_structure_collection(
                challenger_space
            )
            return True
        except MissingStructureError:
            return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        self.child_codelets.append(
            SpaceSelector.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
                challengers=self.losers,
            )
        )
