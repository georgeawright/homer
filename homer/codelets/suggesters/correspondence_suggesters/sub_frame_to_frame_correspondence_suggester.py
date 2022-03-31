from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import exigency, uncorrespondedness
from homer.structures.nodes import Concept


class SubFrameToFrameCorrespondenceSuggester(CorrespondenceSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.correspondence_builders import (
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
        target_view = bubble_chamber.production_views.get(key=exigency)
        target_space_two_candidates = bubble_chamber.new_structure_collection()
        for frame in target_view.matched_sub_frames.keys():
            target_space_two_candidates.add(frame.input_space)
            target_space_two_candidates.add(frame.output_space)
        if len(target_space_two_candidates) == 0:
            raise MissingStructureError
        target_structure_two_candidates = StructureCollection.union(
            *[
                space.contents.where(is_correspondence=False)
                for space in target_space_two_candidates
            ]
        )
        target_structure_two = target_structure_two_candidates.get(
            key=uncorrespondedness
        )
        target_space_two = target_structure_two.parent_space
        urgency = urgency if urgency is not None else target_view.exigency
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
                "target_space_two": target_space_two,
                "target_structure_two": target_structure_two,
            },
            urgency,
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        return cls.make(parent_id, bubble_chamber, urgency)

    def _passes_preliminary_checks(self):
        self.target_space_two = self.target_structure_two.parent_space
        self._get_target_conceptual_space(self, self)
        try:
            if self.target_space_one is None:
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Matched sub frames: {self.target_view.matched_sub_frames}"
                )
                matched_sub_frame_spaces = {}
                for k, v in self.target_view.matched_sub_frames.items():
                    matched_sub_frame_spaces[k.input_space] = v.input_space
                    matched_sub_frame_spaces[k.output_space] = v.output_space
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Matched sub frame spaces: {matched_sub_frame_spaces}"
                )
                frame_two = [
                    frame
                    for frame in self.target_view.matched_sub_frames
                    if self.target_space_two == frame.input_space
                    or self.target_space_two == frame.output_space
                ][0]
                frame_one = self.target_view.matched_sub_frames[frame_two]
                self.target_space_one = (
                    frame_one.input_space
                    if self.target_space_two == frame_two.input_space
                    else frame_one.output_space
                )
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found target space one: {self.target_space_one}"
                )
            if self.target_structure_one is None:
                self._get_target_structure_one(self, self)
        except MissingStructureError:
            return False
        self.parent_concept = self.bubble_chamber.concepts["same"]
        try:
            target_structure_zero = (
                self.target_structure_one.correspondences.filter(
                    lambda x: x.start.parent_space in self.target_view.input_spaces
                )
                .get()
                .start
            )
            if not self.target_view.can_accept_member(
                self.parent_concept,
                self.target_conceptual_space,
                target_structure_zero,
                self.target_structure_two,
            ):
                return False
        except MissingStructureError:
            pass
        can_accept = self.target_view.can_accept_member(
            self.parent_concept,
            self.target_conceptual_space,
            self.target_structure_one,
            self.target_structure_two,
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"View can accept member?: {can_accept}"
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
