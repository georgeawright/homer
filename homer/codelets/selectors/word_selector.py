from homer.codelets.selector import Selector
from homer.codelets.suggesters import WordSuggester
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import uncorrespondedness


class WordSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["word"]

    def _passes_preliminary_checks(self):
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        correspondence_from_frame = StructureCollection(
            {
                correspondence
                for correspondence in self.winners.where(is_correspondence=True)
                if correspondence.start_space.is_frame
            }
        ).get()
        frame = correspondence_from_frame.start_space
        new_target = frame.contents.where(is_word=True).get(key=uncorrespondedness)
        self.child_codelets.append(
            WordSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {
                    "target_view": correspondence_from_frame.parent_view,
                    "target_word": new_target,
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
