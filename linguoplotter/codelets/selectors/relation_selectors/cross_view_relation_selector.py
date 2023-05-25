from linguoplotter.codelets.selectors import RelationSelector
from linguoplotter.codelets.suggesters.relation_suggesters import (
    CrossViewRelationSuggester,
)
from linguoplotter.errors import MissingStructureError


class CrossViewRelationSelector(RelationSelector):
    def _engender_follow_up(self):
        try:
            winner_relation = self.winners.get()
            if winner_relation.parent_space is None:
                return
            target_start = winner_relation.start.parent_space.contents.filter(
                lambda x: x.is_letter_chunk
                and x.members.is_empty
                and len(x.parent_spaces.where(is_conceptual_space=True)) > 1
            ).get()
            target_end = winner_relation.end.parent_space.contents.filter(
                lambda x: x.is_letter_chunk
                and x.members.is_empty
                and x.parent_spaces.where(is_conceptual_space=True)
                == target_start.parent_spaces.where(is_conceptual_space=True)
            ).get()
            targets = self.bubble_chamber.new_dict(
                {
                    "start": target_start,
                    "end": target_end,
                    "start_view": winner_relation.start_view,
                    "end_view": winner_relation.end_view,
                },
                name="targets",
            )
            self.child_codelets.append(
                CrossViewRelationSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    targets,
                    winner_relation.start.unrelatedness,
                )
            )
        except MissingStructureError:
            pass
