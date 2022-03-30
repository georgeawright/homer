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
            else bubble_chamber.focus.view
            if bubble_chamber.focus.view is not None
            else bubble_chamber.views.get(key=activation)
        )
        target_letter_chunk = target_view.parent_frame.output_space.contents.where(
            is_letter_chunk=True
        ).get(key=corresponding_exigency)
        urgency = (
            urgency
            if urgency is not None
            else target_letter_chunk.corresponding_exigency
        )
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
            no_of_parent_spaces = len(
                self.target_projectee.parent_spaces.where(is_contextual_space=True)
            )
            no_of_correspondences = len(self.target_projectee.correspondences)
            if no_of_parent_spaces > 1 and no_of_correspondences < 1:
                self.bubble_chamber.loggers["activity"].log(
                    self, "Not enough correspondences to target projectee"
                )
                return False
            for label in self.target_projectee.labels:
                parent_concept = label.parent_concept
                if parent_concept.is_slot and not parent_concept.is_filled_in:
                    self.bubble_chamber.loggers["activity"].log(
                        self, "Target projectee has label with unfilled parent concept"
                    )
                    return False
            for relation in self.target_projectee.relations.where(
                end=self.target_projectee
            ):
                if (
                    relation.start.is_slot
                    and not relation.start.has_correspondence_to_space(
                        self.target_view.output_space
                    )
                ):
                    self.bubble_chamber.loggers["activity"].log(
                        self, "Target projectee is related to a non projected slot"
                    )
                    return False
        return not self.target_projectee.has_correspondence_to_space(
            self.target_view.output_space
        )
