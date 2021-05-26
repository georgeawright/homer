import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.selectors import PhraseSelector
from homer.codelets.suggesters.phrase_suggesters import PhraseProjectionSuggester
from homer.structure_collection import StructureCollection


class PhraseProjectionSelector(PhraseSelector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        view = bubble_chamber.discourse_views.get_random()
        target_correspondence = view.members.where(
            end_space=view.output_space
        ).get_random()
        target_phrase = target_correspondence.end
        target_correspondences = target_phrase.correspondences.where(end=target_phrase)
        targets = StructureCollection.union(
            target_correspondences, StructureCollection({target_phrase})
        )
        urgency = statistics.fmean([structure.activation for structure in targets])
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    def _passes_preliminary_checks(self):
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        target_view = (
            self.winners.where(is_correspondence=True).get_random().parent_view
        )
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
        return self.champions.where(is_phrase=True).get_random().size

    @property
    def _challengers_size(self):
        return self.challengers.where(is_phrase=True).get_random().size
