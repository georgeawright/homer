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
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {"target_view": target_view, "target_projectee": target_chunk},
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self) -> bool:
        self.target_view = self._target_structures["target_view"]
        self.target_projectee = self._target_structures["target_projectee"]
        self._target_structures["target_correspondence"] = None
        self._target_structures["frame_correspondee"] = None
        self._target_structures["non_frame"] = None
        self._target_structures["non_frame_correspondee"] = None
        return not self.target_projectee.has_correspondence_to_space(
            self.target_view.output_space
        )

    def _calculate_confidence(self):
        self.confidence = 1.0
