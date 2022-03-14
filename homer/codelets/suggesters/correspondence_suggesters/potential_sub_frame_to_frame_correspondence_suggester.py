from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.hyper_parameters import HyperParameters
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation, exigency, uncorrespondedness
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
        non_matched_sub_frame = target_view.parent_frame.sub_frames.filter(
            lambda x: x not in target_view.matched_sub_frames
        ).get(key=uncorrespondedness)
        target_space_two_candidates = bubble_chamber.new_structure_collection(
            non_matched_sub_frame.input_space, non_matched_sub_frame.output_space
        )
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
                "sub_frame": non_matched_sub_frame,
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
        self._get_target_conceptual_space(self, self)
        try:
            views_with_correct_frame = self.bubble_chamber.production_views.filter(
                lambda x: x.parent_frame.parent_concept == self.sub_frame.parent_concept
            )
            self.bubble_chamber.loggers["activity"].log_collection(
                self, views_with_correct_frame, "Views with correct frame"
            )
            views_with_correct_conceptual_space = views_with_correct_frame.filter(
                lambda x: (
                    self.target_conceptual_space
                    in x.parent_frame.input_space.conceptual_spaces
                    if self.target_space_two
                    == self.target_view.parent_frame.input_space
                    else self.target_conceptual_space
                    in x.parent_frame.output_space.conceptual_spaces
                )
                or self.target_conceptual_space is None
            )
            self.bubble_chamber.loggers["activity"].log_collection(
                self, views_with_correct_conceptual_space, "Views with correct space"
            )
            views_that_are_complete = views_with_correct_conceptual_space.filter(
                lambda x: x.unhappiness < HyperParameters.FLOATING_POINT_TOLERANCE
            )
            self.bubble_chamber.loggers["activity"].log_collection(
                self, views_that_are_complete, "Views that are complete"
            )
            self.target_sub_view = views_that_are_complete.get(key=activation)
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found target sub view: {self.target_sub_view}"
            )
            self.target_space_one = (
                self.target_sub_view.parent_frame.input_space
                if self.target_space_two == self.target_view.parent_frame.input_space
                else self.target_sub_view.parent_frame.output_space
            )
            self._get_target_structure_one(self, self)
        except MissingStructureError:
            return False
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

        try:
            return SubFrameToFrameCorrespondenceSuggester.make(
                self.codelet_id, self.bubble_chamber
            )
        except MissingStructureError:
            pass
