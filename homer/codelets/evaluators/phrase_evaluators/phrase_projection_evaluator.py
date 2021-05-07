import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import PhraseEvaluator
from homer.structure_collection import StructureCollection


class PhraseProjectionEvaluator(PhraseEvaluator):
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
        urgency = statistics.fmean(
            [
                concept.activation
                for concept in [
                    bubble_chamber.concepts["phrase"],
                    bubble_chamber.concepts["outer"],
                    bubble_chamber.concepts["forward"],
                    bubble_chamber.concepts["evaluate"],
                ]
            ]
        )
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors.chunk_selectors import PhraseProjectionSelector

        return PhraseProjectionSelector

    def _calculate_confidence(self):
        correspondences = self.target_structures.where(is_correspondence=True)
        target_view = correspondences.get_random().parent_view
        correspondence_starts = StructureCollection(
            {correspondence.start for correspondence in correspondences}
        )
        correspondence_start_1 = correspondence_starts.pop()
        correspondence_start_2 = correspondence_starts.pop()
        correspondence = (
            correspondence_start_1.correspondences_with(correspondence_start_2)
            .where(parent_view=target_view)
            .get_random()
        )
        self.confidence = correspondence.quality
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
