import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.selectors import PhraseSelector
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
        from homer.codelets.builders.phrase_builders import PhraseProjectionBuilder

        self.child_codelets.append(
            PhraseProjectionBuilder.make(self.codelet_id, self.bubble_chamber)
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            )
        )
