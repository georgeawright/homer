from homer.codelets.selectors import PhraseSelector
from homer.codelets.suggesters.phrase_suggesters import PhraseProjectionSuggester


class PhraseProjectionSelector(PhraseSelector):
    def _passes_preliminary_checks(self):
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        target_view = self.winners.where(is_correspondence=True).get().parent_view
        self.child_codelets.append(
            PhraseProjectionSuggester.make(
                self.codelet_id, self.bubble_chamber, target_view=target_view
            )
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            )
        )

    @property
    def _champions_size(self):
        return self.champions.where(is_phrase=True).get().size

    @property
    def _challengers_size(self):
        return self.challengers.where(is_phrase=True).get().size
