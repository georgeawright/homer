from homer.codelets.selector import Selector
from homer.codelets.evaluators import CorrespondenceEvaluator
from homer.errors import MissingStructureError
from homer.structure_collection_keys import activation


class CorrespondenceSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["correspondence"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        champion_correspondence = self.champions.where(is_correspondence=True).get()
        candidates = champion_correspondence.nearby()
        try:
            challenger_correspondence = candidates.get(
                key=activation, exclude=[champion_correspondence]
            )
            self.challengers = self.bubble_chamber.new_structure_collection(
                challenger_correspondence
            )
        except MissingStructureError:
            pass
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        from homer.codelets.suggesters import CorrespondenceSuggester

        self.child_codelets.append(
            CorrespondenceEvaluator.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            )
        )
        winner_correspondence = self.winners.where(is_correspondence=True).get()
        target_view = winner_correspondence.parent_view
        try:
            self.child_codelets.append(
                CorrespondenceSuggester.make(
                    self.codelet_id,
                    self.bubble_chamber,
                    target_view=target_view,
                    urgency=target_view.exigency,
                )
            )
        except MissingStructureError:
            pass
