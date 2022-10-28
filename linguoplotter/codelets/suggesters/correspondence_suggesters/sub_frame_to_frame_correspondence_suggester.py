from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import CorrespondenceSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collection import StructureCollection
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
        if self.target_space_two is None:
            self.target_space_two = (
                self.sub_frame.input_space
                if self.target_space_two.has_location_in_space(
                    self.sub_frame.input_space
                )
                else self.sub_frame.output_space
            )
        self._get_target_conceptual_space(self, self)
        if self.target_structure_one is not None and self.parent_concept is not None:
            classification = self.parent_concept.classifier.classify(
                concept=self.parent_concept,
                space=self.target_conceptual_space,
                start=self.target_structure_one,
                end=self.target_structure_two,
                view=self.target_view,
            )
            if classification < 0.5:
                self.parent_concept = self.bubble_chamber.new_compound_concept(
                    self.bubble_chamber.concepts["not"], [self.parent_concept]
                )
        else:
            self.parent_concept = self.bubble_chamber.concepts["same"]
        try:
            if self.target_space_one is None:
                matched_sub_frame_spaces = {}
                for k, v in self.target_view.matched_sub_frames.items():
                    matched_sub_frame_spaces[k.input_space] = v.input_space
                    matched_sub_frame_spaces[k.output_space] = v.output_space
                frame_two = [
                    frame
                    for frame in self.target_view.matched_sub_frames
                    if (
                        frame.input_space in self.target_structure_two.parent_spaces
                        and not self.target_structure_two.has_correspondence_to_space(
                            frame.input_space
                        )
                    )
                    or (
                        frame.output_space in self.target_structure_two.parent_spaces
                        and not self.target_structure_two.has_correspondence_to_space(
                            frame.output_space
                        )
                    )
                ][0]
                frame_one = self.target_view.matched_sub_frames[frame_two]
                self.target_space_one = (
                    frame_one.input_space
                    if frame_one.input_space.parent_concept
                    == self.target_space_two.parent_concept
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
