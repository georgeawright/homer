from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import ProjectionSuggester
from homer.structure_collection_keys import activation, corresponding_exigency
from homer.structures import View


class LetterChunkProjectionSuggester(ProjectionSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.projection_builders import (
            LetterChunkProjectionBuilder,
        )

        return LetterChunkProjectionBuilder

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
            else bubble_chamber.views.get(key=activation)
        )
        frame = target_view.input_spaces.where(is_frame=True).get()
        target_letter_chunk = frame.contents.where(is_chunk=True).get(
            key=corresponding_exigency
        )
        urgency = urgency if urgency is not None else target_view.activation
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {"target_view": target_view, "target_projectee": target_letter_chunk},
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["letter-chunk"]

    def _passes_preliminary_checks(self) -> bool:
        if self.target_projectee.is_slot:
            for link in self.target_projectee.links:
                if link.parent_concept.is_slot and not link.parent_concept.is_filled_in:
                    return False
        return not self.target_projectee.has_correspondence_to_space(
            self.target_view.output_space
        )
