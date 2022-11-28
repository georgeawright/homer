from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import ProjectionSuggester
from linguoplotter.structure_collection_keys import activation, corresponding_exigency
from linguoplotter.structures import View


class ChunkProjectionSuggester(ProjectionSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.projection_builders import (
            ChunkProjectionBuilder,
        )

        return ChunkProjectionBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View = None,
        urgency: float = None,
    ):
        target_view = (
            target_view
            if target_view is not None
            else bubble_chamber.focus.view
            if bubble_chamber.focus.view is not None
            else bubble_chamber.views.get(key=activation)
        )
        frame = target_view.input_spaces.where(is_frame=True).get()
        target_chunk = frame.contents.where(is_chunk=True).get(
            key=corresponding_exigency
        )
        urgency = urgency if urgency is not None else target_view.activation
        targets = bubble_chamber.new_dict(
            {"view": target_view, "projectee": target_chunk}, name="targets"
        )
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self) -> bool:
        return not self.targets["projectee"].has_correspondence_to_space(
            self.targets["view"].output_space
        )

    def _calculate_confidence(self):
        self.confidence = 1.0
