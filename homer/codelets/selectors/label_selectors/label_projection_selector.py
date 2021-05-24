import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.selectors import LabelSelector
from homer.codelets.suggesters.label_suggesters import LabelProjectionSuggester
from homer.structure_collection import StructureCollection


class LabelProjectionSelector(LabelSelector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target_view = bubble_chamber.monitoring_views.get_active()
        target_label = target_view.interpretation_space.contents.where(
            is_label=True
        ).get_random()
        target_correspondence = target_label.correspondences_to_space(
            target_view.text_space
        ).get_random()
        target_structures = StructureCollection({target_label, target_correspondence})
        urgency = statistics.fmean(
            [structure.activation for structure in target_structures]
        )
        return cls.spawn(parent_id, bubble_chamber, target_structures, urgency)

    def _passes_preliminary_checks(self):
        return True

    def _fizzle(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        target_view = (
            self.winners.where(is_correspondence=True).get_random().parent_view
        )
        self.child_codelets.append(
            LabelProjectionSuggester.make(
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
