from homer.bubble_chamber import BubbleChamber
from homer.codelets.selector import Selector
from homer.structure_collection import StructureCollection


class WordSelector(Selector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        word = bubble_chamber.words.get_active()
        correspondences = word.correspondences.where(end=word)
        champions = StructureCollection.union(
            StructureCollection({word}), correspondences
        )
        return cls.spawn(parent_id, bubble_chamber, champions, word.activation)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["word"]

    def _passes_preliminary_checks(self):
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        from homer.codelets.builders import WordBuilder

        correspondence_from_frame = StructureCollection(
            {
                correspondence
                for correspondence in self.winners.where(is_correspondence=True)
                if correspondence.start_space.is_frame
            }
        ).get_random()
        frame = correspondence_from_frame.start_space
        new_target = frame.contents.where(is_word=True).get_unhappy()
        self.child_codelets.append(
            WordBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                correspondence_from_frame.parent_view,
                new_target,
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
