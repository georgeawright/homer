from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import CorrespondenceSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structure_collection_keys import (
    activation,
    exigency,
    uncorrespondedness,
)
from linguoplotter.structures.nodes import Concept


class PotentialSubFrameToFrameCorrespondenceSuggester(CorrespondenceSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.correspondence_builders import (
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
        if self.target_conceptual_space is None:
            self._get_target_conceptual_space(self, self)
        if self.target_space_one is None:
            try:
                PotentialSubFrameToFrameCorrespondenceSuggester._get_target_space_one(
                    self, self
                )
                PotentialSubFrameToFrameCorrespondenceSuggester._get_target_structure_one(
                    self, self
                )
            except MissingStructureError:
                return False
        self.parent_concept = self.bubble_chamber.concepts["same"]
        for correspondence in self.target_sub_view.members:
            if not self.target_view.can_accept_member(
                correspondence.parent_concept,
                correspondence.conceptual_space,
                correspondence.start,
                correspondence.end,
                sub_view=self.target_sub_view,
            ):
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Target view cannot accept {correspondence}"
                )
                return False
        if not self.target_view.can_accept_member(
            self.parent_concept,
            self.target_conceptual_space,
            self.target_structure_one,
            self.target_structure_two,
            sub_view=self.target_sub_view,
        ):
            self.bubble_chamber.loggers["activity"].log(
                self, "View cannot accept correspondence from target one"
            )
            return False
        return True

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

    @staticmethod
    def _get_target_space_one(calling_codelet, correspondence_suggester):
        bubble_chamber = correspondence_suggester.bubble_chamber
        views_with_correct_frame = bubble_chamber.production_views.filter(
            lambda x: x.parent_frame.parent_concept
            == correspondence_suggester.sub_frame.parent_concept
            and x.super_views.is_empty()
        )
        bubble_chamber.loggers["activity"].log_collection(
            calling_codelet, views_with_correct_frame, "Views with correct frame"
        )
        views_with_correct_conceptual_space = views_with_correct_frame.filter(
            lambda x: (
                correspondence_suggester.target_conceptual_space
                in x.parent_frame.input_space.conceptual_spaces
                if correspondence_suggester.target_space_two
                == correspondence_suggester.target_view.parent_frame.input_space
                else correspondence_suggester.target_conceptual_space
                in x.parent_frame.output_space.conceptual_spaces
            )
            or correspondence_suggester.target_conceptual_space is None
        )
        bubble_chamber.loggers["activity"].log_collection(
            calling_codelet,
            views_with_correct_conceptual_space,
            "Views with correct space",
        )
        correspondence_suggester.target_sub_view = (
            views_with_correct_conceptual_space.get(key=activation)
        )
        bubble_chamber.loggers["activity"].log(
            calling_codelet,
            f"Found target sub view: {correspondence_suggester.target_sub_view}",
        )
        correspondence_suggester.target_space_one = (
            correspondence_suggester.target_sub_view.parent_frame.input_space
            if correspondence_suggester.target_sub_view.parent_frame.input_space.parent_concept
            == correspondence_suggester.target_space_two.parent_concept
            else correspondence_suggester.target_sub_view.parent_frame.output_space
        )
        bubble_chamber.loggers["activity"].log(
            calling_codelet,
            f"Found target space one: {correspondence_suggester.target_space_one}",
        )
