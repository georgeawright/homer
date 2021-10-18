from homer.codelets.selectors import ProjectionSelector
from homer.codelets.suggesters.projection_suggesters import WordProjectionSuggester
from homer.structure_collection_keys import uncorrespondedness


class WordProjectionSelector(ProjectionSelector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["word"]

    def _passes_preliminary_checks(self):
        return True

    def _engender_follow_up(self):
        correspondence_from_frame = self.bubble_chamber.new_structure_collection(
            *[
                correspondence
                for correspondence in self.winners.where(is_correspondence=True)
                if correspondence.start.parent_space.parent_concept
                == correspondence.end.parent_space.parent_concept
            ]
        ).get()
        frame = correspondence_from_frame.start.parent_space
        new_target = frame.contents.where(is_word=True).get(key=uncorrespondedness)
        self.child_codelets.append(
            WordProjectionSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {
                    "target_view": correspondence_from_frame.parent_view,
                    "target_projectee": new_target,
                },
                new_target.unhappiness,
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
