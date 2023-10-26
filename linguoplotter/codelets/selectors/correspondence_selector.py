from linguoplotter.codelets.selector import Selector
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection_keys import activation


class CorrespondenceSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["correspondence"]

    def _passes_preliminary_checks(self):
        if self.challengers.not_empty:
            return True
        champion = self.champions.get()
        candidates = champion.nearby()
        try:
            self.challengers.add(candidates.get(key=activation, exclude=[champion]))
        except MissingStructureError:
            pass
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        from linguoplotter.codelets.suggesters import CorrespondenceSuggester

        try:
            winner_correspondence = self.winners.get()
            target_view = winner_correspondence.parent_view
            self.child_codelets.append(
                CorrespondenceSuggester.make(
                    self.codelet_id,
                    self.bubble_chamber,
                    target_view=target_view,
                    urgency=target_view.salience,
                )
            )
        except MissingStructureError:
            pass
