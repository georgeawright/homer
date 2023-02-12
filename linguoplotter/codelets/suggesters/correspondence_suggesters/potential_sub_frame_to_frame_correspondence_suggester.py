from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import CorrespondenceSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collections import StructureSet
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
        target_space_two_candidates = bubble_chamber.new_set(
            non_matched_sub_frame.input_space, non_matched_sub_frame.output_space
        )
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
            {
                "target_view": target_view,
                "end": end,
                "sub_frame": non_matched_sub_frame,
            },
            name="targets",
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
        if self.targets["space"] is None:
            self._get_target_conceptual_space(self, self)
        if (
            self.targets["start"] is not None
            and self.targets["concept"] is not None
            and self.targets["view"].members.not_empty
        ):
            if self.targets["sub_frame"] in self.targets["view"].matched_sub_frames:
                self.bubble_chamber.loggers["activity"].log_set(
                    self.targets["view"].matched_sub_frames, "matched sub frames"
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
        for correspondence in self.targets["sub_view"].members:
            if not self.targets["view"].can_accept_member(
                correspondence.parent_concept,
                correspondence.conceptual_space,
                correspondence.start,
                correspondence.end,
                sub_view=self.targets["sub_view"],
            ):
                self.bubble_chamber.loggers["activity"].log(
                    f"Target view cannot accept {correspondence}"
                )
                return False
        if not self.targets["view"].can_accept_member(
            self.targets["concept"],
            self.targets["space"],
            self.targets["start"],
            self.targets["end"],
            sub_view=self.targets["sub_view"],
        ):
            self.bubble_chamber.loggers["activity"].log(
                "View cannot accept correspondence from target start"
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
    def _get_target_space_one(parent_codelet, child_codelet):
        bubble_chamber = parent_codelet.bubble_chamber
        target_view = child_codelet.targets["view"]
        compatible_sub_views = bubble_chamber.views.filter(
            lambda x: x != target_view
            and (
                x.unhappiness < parent_codelet.FLOATING_POINT_TOLERANCE
                and not any(
                    [
                        x.raw_input_nodes == v.raw_input_nodes
                        for v in target_view.sub_views
                    ]
                )
            )
            if x.parent_frame.parent_concept.location_in_space(
                bubble_chamber.spaces["grammar"]
            )
            == bubble_chamber.concepts["sentence"].location_in_space(
                bubble_chamber.spaces["grammar"]
            )
            else True
            and x.super_views.is_empty
            and (
                x.parent_frame.parent_concept
                == child_codelet.targets["sub_frame"].parent_concept
            )
            and (x.parent_frame.progenitor != target_view.parent_frame.progenitor)
            and (x.input_spaces == target_view.input_spaces)
            and x.members.filter(
                lambda c: c.parent_concept.is_compound_concept
            ).is_empty
            and all(
                [
                    target_view.can_accept_member(
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
            lambda x: x.members.is_empty
            or any(
                [
                    target_view.can_accept_member(
                        member.parent_concept,
                        member.conceptual_space,
                        member.start,
                        child_codelet.targets["end"],
                        sub_view=x,
                    )
                    and target_view.can_accept_member(
                        member.parent_concept,
                        member.conceptual_space,
                        member.end,
                        child_codelet.targets["end"],
                        sub_view=x,
                    )
                    for member in x.members.filter(
                        lambda c: type(c.start) == type(child_codelet.targets["end"])
                        and c.start.parent_space.parent_concept
                        == child_codelet.targets["end"].parent_space.parent_concept
                    )
                ]
            )
        )
        bubble_chamber.loggers["activity"].log_set(
            views_with_compatible_nodes, "Compatible sub views"
        )
        child_codelet.targets["sub_view"] = views_with_compatible_nodes.get(
            key=lambda x: fuzzy.OR(
                x.exigency,
                max(
                    [
                        x.cohesiveness_with(sub_view)
                        for sub_view in target_view.sub_views
                    ]
                ),
            )
            if target_view.sub_views.not_empty
            else x.exigency
        )
        child_codelet.targets["start_space"] = (
            child_codelet.targets["sub_view"].parent_frame.input_space
            if child_codelet.targets["sub_view"].parent_frame.input_space.parent_concept
            == child_codelet.targets["end"].parent_space.parent_concept
            else child_codelet.targets["sub_view"].parent_frame.output_space
        )
