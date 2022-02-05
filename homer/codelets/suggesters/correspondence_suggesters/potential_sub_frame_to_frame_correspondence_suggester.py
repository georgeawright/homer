from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection_keys import activation, corresponding_exigency, exigency
from homer.structures.nodes import Concept


class PotentialSubFrameToFrameCorrespondenceSuggester(CorrespondenceSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.correspondence_builders import (
            PotentialSubFrameToFrameCorrespondenceBuilder,
        )

        return PotentialSubFrameToFrameCorrespondenceBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.production_views.get(key=exigency)
        urgency = urgency if urgency is not None else target_view.exigency
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
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
        try:
            # TODO: possibly pick a sub view with high corresponding exigency first
            sub_view = self.bubble_chamber.production_views.filter(
                lambda x: x.parent_frame.parent_concept
                in {
                    frame.parent_concept
                    for frame in self.target_view.parent_frame.sub_frames
                }
            ).get(key=activation)
            frame_one = sub_view.parent_frame
            spaces = self.bubble_chamber.new_structure_collection(
                frame_one.input_space, frame_one.output_space
            )
            self.target_space_one = spaces.get(key=corresponding_exigency)
            self.target_structure_one = self.target_space_one.contents.where(
                is_correspondence=False
            ).get(key=corresponding_exigency)
            self.sub_frame = self.target_view.parent_frame.sub_frames.filter(
                lambda x: x.parent_concept == frame_one.parent_concept
                and x not in self.target_view.matched_sub_frames
            ).get(key=corresponding_exigency)
            self.target_space_two = (
                self.sub_frame.input_space
                if self.target_space_one == frame_one.input_space
                else self.sub_frame.output_space
            )
            self.target_structure_two = self.target_space_two.contents.of_type(
                type(self.target_structure_one)
            ).get(key=lambda x: x.similarity_with(self.target_structure_one))
        except MissingStructureError:
            return False
        self.target_conceptual_space = (
            self.target_structure_one.parent_concept.parent_space
            if self.target_structure_one.is_link
            else None
        )
        self.parent_concept = self.bubble_chamber.concepts["same"]
        return self.target_view.can_accept_member(
            self.parent_concept,
            self.target_conceptual_space,
            self.target_structure_one,
            self.target_structure_two,
        )

    def _fizzle(self):
        from .sub_frame_to_frame_correspondence_suggester import (
            SubFrameToFrameCorrespondenceSuggester,
        )

        return SubFrameToFrameCorrespondenceSuggester.make(
            self.codelet_id, self.bubble_chamber
        )
