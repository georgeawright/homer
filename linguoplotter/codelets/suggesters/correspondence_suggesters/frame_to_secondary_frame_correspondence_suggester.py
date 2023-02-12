from linguoplotter.codelets.suggesters import CorrespondenceSuggester
from linguoplotter.errors import MissingStructureError


class FrameToSecondaryFrameCorrespondenceSuggester(CorrespondenceSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.correspondence_builders import (
            FrameToSecondaryFrameCorrespondenceBuilder,
        )

        return FrameToSecondaryFrameCorrespondenceBuilder

    def _passes_preliminary_checks(self):
        self._get_target_conceptual_space(self, self)
        if self.targets["start"] is not None and self.targets["concept"] is not None:
            if self.targets["space"] is not None and self.targets["space"].is_slot:
                classification_space = (
                    self.targets["start"].parent_concept.parent_space
                    if self.targets["end"].is_label
                    else self.targets["start"].conceptual_space
                )
            else:
                classification_space = self.targets["space"]
            classification = self.targets["concept"].classifier.classify(
                concept=self.targets["concept"],
                space=classification_space,
                start=self.targets["start"],
                end=self.targets["end"],
                view=self.targets["view"],
            )
            if classification < 0.5:
                self.targets["concept"] = self.bubble_chamber.new_compound_concept(
                    self.bubble_chamber.concepts["not"], [self.targets["concept"]]
                )
        else:
            self.targets["concept"] = self.bubble_chamber.concepts["same"]
        try:
            if self.targets["start_space"] is None:
                matched_secondary_frame_spaces = {}
                for k, v in self.targets["view"].matched_secondary_sub_frames.items():
                    matched_secondary_frame_spaces[k.input_space] = v.input_space
                    matched_secondary_frame_spaces[k.output_space] = v.output_space
                frame_two = [
                    frame
                    for frame in self.targets["view"].matched_secondary_sub_frames
                    if (
                        frame.input_space in self.targets["end"].parent_spaces
                        and not self.targets["end"].has_correspondence_to_space(
                            frame.input_space
                        )
                    )
                    or (
                        frame.output_space in self.targets["end"].parent_spaces
                        and not self.targets["end"].has_correspondence_to_space(
                            frame.output_space
                        )
                    )
                ][0]
                frame_one = self.targets["view"].matched_secondary_sub_frames[frame_two]
                self.targets["start_space"] = (
                    frame_one.input_space
                    if frame_one.input_space.parent_concept
                    == self.targets["end"].parent_space.parent_concept
                    else frame_one.output_space
                )
            if self.targets["start"] is None:
                self._get_target_structure_one(self, self)
        except MissingStructureError:
            return False
        self.targets["concept"] = self.bubble_chamber.concepts["same"]
        can_accept = self.targets["view"].can_accept_member(
            self.targets["concept"],
            self.targets["space"],
            self.targets["start"],
            self.targets["end"],
        )
        self.bubble_chamber.loggers["activity"].log(
            f"View can accept member?: {can_accept}"
        )
        return can_accept

    def _fizzle(self):
        pass
