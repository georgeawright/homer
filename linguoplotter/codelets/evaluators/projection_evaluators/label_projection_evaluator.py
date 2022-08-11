from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluators import ProjectionEvaluator
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection import StructureCollection


class LabelProjectionEvaluator(ProjectionEvaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors.projection_selectors import (
            LabelProjectionSelector,
        )

        return LabelProjectionSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["label"]
        input_concept = bubble_chamber.concepts["input"]
        view = bubble_chamber.new_structure_collection(
            *[
                view
                for view in bubble_chamber.views
                if view.output_space.parent_concept == input_concept
                and not view.contents.where(is_label=True).is_empty()
            ]
        ).get()
        label = view.ouptut_space.contents.where(is_label=True).get()
        correspondences = label.correspondences.where(end=label)
        if correspondences.is_empty():
            raise MissingStructureError
        target_structures = StructureCollection.union(
            bubble_chamber.new_structure_collection(label), correspondences
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            target_structures,
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["label"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        label = self.target_structures.where(is_label=True).get()
        try:
            # TODO: out of date
            non_frame_item = (
                self.target_structures.where(is_correspondence=True)
                .filter(lambda x: not x.start.is_slot)
                .get()
                .start
            )
            frame_item = (
                self.target_structures.where(is_correspondence=True)
                .filter(lambda x: x.start.is_slot)
                .get()
                .start
            )
            correspondence_to_frame = non_frame_item.correspondences_with(
                frame_item
            ).get()
            self.confidence = fuzzy.AND(
                non_frame_item.quality, correspondence_to_frame.quality
            )
        except MissingStructureError:
            self.confidence = 1.0
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - label.activation
