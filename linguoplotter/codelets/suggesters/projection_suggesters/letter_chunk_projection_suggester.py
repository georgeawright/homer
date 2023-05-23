from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import ProjectionSuggester
from linguoplotter.structure_collection_keys import activation, corresponding_salience
from linguoplotter.structures import View


class LetterChunkProjectionSuggester(ProjectionSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.projection_builders import (
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
        frame = target_view.parent_frame
        target_letter_chunk = frame.output_space.contents.where(
            is_letter_chunk=True
        ).get(key=corresponding_salience)
        urgency = (
            urgency
            if urgency is not None
            else target_letter_chunk.corresponding_salience
        )
        targets = bubble_chamber.new_dict(
            {"view": target_view, "frame": frame, "projectee": target_letter_chunk},
            name="targets",
        )
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["letter-chunk"]

    def _passes_preliminary_checks(self) -> bool:
        if self.targets["projectee"].is_slot:
            if (
                len(
                    self.targets["projectee"].parent_spaces.where(
                        is_contextual_space=True
                    )
                )
                > 1
                and self.targets["projectee"].correspondences.is_empty
            ):
                self.bubble_chamber.loggers["activity"].log(
                    "mismatch between parent spaces and correspondences"
                )
                return False
            try:
                node_group = [
                    group
                    for group in self.targets["view"].node_groups
                    if self.targets["projectee"] in group.values()
                ][0]
                nodes_with_name = [node for node in node_group if node.name is not None]
                if len(nodes_with_name) == 0:
                    self.bubble_chamber.loggers["activity"].log(
                        "No correspondees with name"
                    )
                    return False
            except IndexError:
                pass
            for label in self.targets["projectee"].labels:
                parent_concept = label.parent_concept
                if parent_concept.is_slot and not parent_concept.is_filled_in:
                    if self.targets["view"].parent_frame.input_space.contents.where(
                        is_link=True, parent_concept=parent_concept
                    ):
                        self.bubble_chamber.loggers["activity"].log(
                            "Target projectee has label with unfilled parent concept"
                        )
                        return False
            for relation in self.targets["projectee"].relations.where(
                end=self.targets["projectee"]
            ):
                if (
                    relation.start.is_slot
                    and not relation.start.has_correspondence_to_space(
                        self.targets["view"].output_space
                    )
                ):
                    self.bubble_chamber.loggers["activity"].log(
                        "Target projectee is related to a non projected slot"
                    )
                    return False
        return not self.targets["projectee"].has_correspondence_to_space(
            self.targets["view"].output_space
        )
