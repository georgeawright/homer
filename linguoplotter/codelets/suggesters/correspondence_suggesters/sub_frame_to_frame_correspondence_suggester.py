from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import CorrespondenceSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structure_collection_keys import exigency, uncorrespondedness
from linguoplotter.structures.nodes import Concept


class SubFrameToFrameCorrespondenceSuggester(CorrespondenceSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.correspondence_builders import (
            SubFrameToFrameCorrespondenceBuilder,
        )

        return SubFrameToFrameCorrespondenceBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.views.get(key=exigency)
        target_space_two_candidates = bubble_chamber.new_set()
        for frame in target_view.matched_sub_frames.keys():
            target_space_two_candidates.add(frame.input_space)
            target_space_two_candidates.add(frame.output_space)
        if len(target_space_two_candidates) == 0:
            raise MissingStructureError
        end_candidates = StructureSet.union(
            *[
                space.contents.where(is_correspondence=False)
                for space in target_space_two_candidates
            ]
        )
        end = end_candidates.get(key=uncorrespondedness)
        urgency = urgency if urgency is not None else target_view.exigency
        targets = bubble_chamber.new_dict(
            {"target_view": target_view, "end": end}, name="targets"
        )
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        return cls.make(parent_id, bubble_chamber, urgency)

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
                matched_sub_frame_spaces = {}
                for k, v in self.targets["view"].matched_sub_frames.items():
                    matched_sub_frame_spaces[k.input_space] = v.input_space
                    matched_sub_frame_spaces[k.output_space] = v.output_space
                frame_two = [
                    frame
                    for frame in self.targets["view"].matched_sub_frames
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
                frame_one = self.targets["view"].matched_sub_frames[frame_two]
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
        from .space_to_frame_correspondence_suggester import (
            SpaceToFrameCorrespondenceSuggester,
        )

        try:
            return SpaceToFrameCorrespondenceSuggester.make(
                self.codelet_id, self.bubble_chamber
            )
        except MissingStructureError:
            pass
