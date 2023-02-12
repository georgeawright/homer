from linguoplotter.codelets.suggesters import CorrespondenceSuggester
from linguoplotter.errors import MissingStructureError


class PotentialFrameToSecondaryFrameCorrespondenceSuggester(CorrespondenceSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.correspondence_builders import (
            PotentialFrameToSecondaryFrameCorrespondenceBuilder,
        )

        return PotentialFrameToSecondaryFrameCorrespondenceBuilder

    def _passes_preliminary_checks(self):
        self.targets["end_frame"] = (
            self.targets["frame"]
            .sub_frames.filter(
                lambda x: self.targets["end"].parent_space
                in [x.input_space, x.output_space]
            )
            .get()
        )
        if self.targets["space"] is None:
            self._get_target_conceptual_space(self, self)
        if (
            self.targets["start"] is not None
            and self.targets["concept"] is not None
            and self.targets["view"].members.not_empty
        ):
            if (
                self.targets["end_frame"]
                in self.targets["view"].matched_secondary_sub_frames
            ):
                self.bubble_chamber.loggers["activity"].log_set(
                    self.targets["view"].matched_secondary_sub_frames,
                    "matched secondary sub frames",
                )
                return False
            if self.targets["space"] is not None and self.targets["space"].is_slot:
                classification_space = (
                    self.targets["start"].parent_concept.parent_space
                    if self.targets["end"].is_label
                    else self.targets["start"].conceptual_space
                )
                if classification_space.is_slot:
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
            self.bubble_chamber.loggers["activity"].log(
                f"Preliminary classification: {classification}"
            )
            if classification < 0.5:
                self.targets["concept"] = self.bubble_chamber.new_compound_concept(
                    self.bubble_chamber.concepts["not"], [self.targets["concept"]]
                )
        else:
            self.targets["concept"] = self.bubble_chamber.concepts["same"]
        if self.targets["start_space"] is None:
            try:
                self._get_target_space_one(self, self)
                self._get_target_structure_one(self, self)
            except MissingStructureError:
                return False
        if not self.targets["view"].can_accept_member(
            self.targets["concept"],
            self.targets["space"],
            self.targets["start"],
            self.targets["end"],
        ):
            self.bubble_chamber.loggers["activity"].log(
                "View cannot accept correspondence from target start"
            )
            return False
        return True

    @staticmethod
    def _get_target_space_one(parent_codelet, child_codelet):
        target_view = child_codelet.targets["view"]
        target_frame = child_codelet.targets["frame"]
        target_end = child_codelet.targets["end"]
        start_frame = target_view.parent_frame.sub_frames.filter(
            lambda x: x.parent_concept == target_frame.parent_concept
        ).get()
        child_codelet.targets["start_space"] = (
            start_frame.input_space
            if start_frame.input_space.parent_concept
            == target_end.parent_space.parent_concept
            else start_frame.output_space
        )
