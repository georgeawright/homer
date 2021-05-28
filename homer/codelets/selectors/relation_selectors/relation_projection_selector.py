from homer.codelets.selectors import RelationSelector
from homer.codelets.suggesters.relation_suggesters import RelationProjectionSuggester


class RelationProjectionSelector(RelationSelector):
    def _passes_preliminary_checks(self):
        return True

    def _fizzle(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        target_view = self.winners.where(is_correspondence=True).get().parent_view
        self.child_codelets.append(
            RelationProjectionSuggester.make(
                self.codelet_id,
                self.bubble_chamber,
                target_view=target_view,
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
