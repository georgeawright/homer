from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import CorrespondenceSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structure_collection_keys import (
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
        target_view = bubble_chamber.views.get(key=exigency)
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
        if (
            self.target_structure_one is not None
            and self.parent_concept is not None
            and not self.target_view.members.is_empty()
        ):
            if (
                self.target_conceptual_space is not None
                and self.target_conceptual_space.is_slot
            ):
                classification_space = (
                    self.target_structure_one.parent_concept.parent_space
                    if self.target_structure_two.is_label
                    else self.target_structure_one.conceptual_space
                )
            else:
                classification_space = self.target_conceptual_space
            classification = self.parent_concept.classifier.classify(
                concept=self.parent_concept,
                space=classification_space,
                start=self.target_structure_one,
                end=self.target_structure_two,
                view=self.target_view,
            )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Preliminary classification: {classification}"
            )
            if classification < 0.5:
                self.parent_concept = self.bubble_chamber.new_compound_concept(
                    self.bubble_chamber.concepts["not"], [self.parent_concept]
                )
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found parent concept: {self.parent_concept}"
                )
        else:
            self.parent_concept = self.bubble_chamber.concepts["same"]
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found parent concept: {self.parent_concept}"
            )
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
        compatible_sub_views = bubble_chamber.views.filter(
            lambda x: x != correspondence_suggester.target_view
            and x.super_views.is_empty()
            and (
                x.parent_frame.parent_concept
                == correspondence_suggester.sub_frame.parent_concept
            )
            and (
                x.parent_frame.progenitor
                != correspondence_suggester.target_view.parent_frame.progenitor
            )
            and (x.input_spaces == correspondence_suggester.target_view.input_spaces)
            and all(
                [
                    any(
                        [
                            super_frame_space.subsumes(sub_frame_space)
                            for sub_frame_space in x.parent_frame.input_space.conceptual_spaces
                        ]
                    )
                    for super_frame_space in correspondence_suggester.sub_frame.input_space.conceptual_spaces
                ]
            )
            and all(
                [
                    any(
                        [
                            super_frame_space.subsumes(sub_frame_space)
                            for sub_frame_space in x.parent_frame.output_space.conceptual_spaces
                        ]
                    )
                    for super_frame_space in correspondence_suggester.sub_frame.output_space.conceptual_spaces
                ]
            )
            and all(
                [
                    correspondence_suggester.target_view.can_accept_member(
                        member.parent_concept,
                        member.conceptual_space,
                        member.start,
                        member.end,
                        sub_view=x,
                    )
                    for member in x.members
                ]
            )
        )
        views_with_compatible_nodes = compatible_sub_views.filter(
            lambda x: x.members.is_empty()
            or any(
                [
                    correspondence_suggester.target_view.can_accept_member(
                        member.parent_concept,
                        member.conceptual_space,
                        member.start,
                        correspondence_suggester.target_structure_two,
                        sub_view=x,
                    )
                    and correspondence_suggester.target_view.can_accept_member(
                        member.parent_concept,
                        member.conceptual_space,
                        member.end,
                        correspondence_suggester.target_structure_two,
                        sub_view=x,
                    )
                    for member in x.members.filter(
                        lambda c: type(c.start)
                        == type(correspondence_suggester.target_structure_two)
                        and c.start.parent_space.parent_concept
                        == correspondence_suggester.target_structure_two.parent_space.parent_concept
                    )
                ]
            )
        )
        bubble_chamber.loggers["activity"].log_collection(
            calling_codelet, views_with_compatible_nodes, "Compatible sub views"
        )
        correspondence_suggester.target_sub_view = views_with_compatible_nodes.get(
            key=exigency
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
