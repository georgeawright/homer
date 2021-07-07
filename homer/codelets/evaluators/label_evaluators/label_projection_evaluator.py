import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import LabelEvaluator
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation


class LabelProjectionEvaluator(LabelEvaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target_view = bubble_chamber.monitoring_views.get(key=activation)
        target_label = target_view.interpretation_space.contents.where(
            is_label=True
        ).get()
        target_correspondence = target_label.correspondences_to_space(
            target_view.text_space
        ).get()
        target_structures = StructureCollection({target_label, target_correspondence})
        urgency = statistics.fmean(
            [
                concept.activation
                for concept in [
                    bubble_chamber.concepts["label"],
                    bubble_chamber.concepts["outer"],
                    bubble_chamber.concepts["forward"],
                    bubble_chamber.concepts["evaluate"],
                ]
            ]
        )
        return cls.spawn(parent_id, bubble_chamber, target_structures, urgency)

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors.label_selectors import LabelProjectionSelector

        return LabelProjectionSelector

    def _calculate_confidence(self):
        target_correspondence = self.target_structures.where(
            is_correspondence=True
        ).get()
        self.confidence = target_correspondence.start.quality
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
