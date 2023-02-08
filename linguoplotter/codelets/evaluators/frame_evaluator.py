from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.evaluator import Evaluator
from linguoplotter.structure_collection_keys import activation
from linguoplotter.structure_collections import StructureSet


class FrameEvaluator(Evaluator):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        view = bubble_chamber.views.filter(lambda x: x.secondary_frames.not_empty).get(
            key=activation
        )
        frame = view.secondary_frames.get(key=lambda x: abs(x.activation - x.quality))
        targets = bubble_chamber.new_set(frame, name="targets")
        return cls.spawn(
            parent_id,
            bubble_chamber,
            targets,
            abs(frame.activation - frame.quality),
        )

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.selectors import FrameSelector

        return FrameSelector

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["frame"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        target_frame = self.targets.get()
        correspondences = StructureSet.union(
            target_frame.input_space.contents.where(is_correspondence=True),
            target_frame.output_space.contents.where(is_correspondence=True),
        )
        if any(
            [
                correspondence.parent_concept.is_compound_concept
                and correspondence.parent_concept.root.name == "not"
                for correspondence in correspondences
            ]
        ):
            self.confidence = 0.0
        else:
            total_slots = (
                len(correspondences) + target_frame.number_of_items_left_to_process
            )
            self.confidence = (
                sum(correspondence.quality for correspondence in correspondences)
                / total_slots
            )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
        self.activation_difference = self.confidence - target_frame.activation
