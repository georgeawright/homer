from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters.view_suggester import (
    BottomUpCohesionViewSuggester,
)
from linguoplotter.errors import MissingStructureError


class MergedFrameViewSuggester(BottomUpCohesionViewSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.view_builders import MergedFrameViewBuilder

        return MergedFrameViewBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: float = None,
    ):
        targets = bubble_chamber.new_dict(name="targets")
        if urgency is None:
            number_of_merged_frame_views = len(
                bubble_chamber.views.filter(
                    lambda x: x.parent_frame.progenitor.is_merged_frame
                )
            )
            number_of_views_with_mergeable_frames = len(
                bubble_chamber.views.filter(
                    lambda x: x.parent_frame.progenitor.relations.where(
                        parent_concept=bubble_chamber.concepts["more"],
                        conceptual_space=bubble_chamber.spaces["grammar"],
                    ).not_empty
                )
            )
            try:
                urgency = 1 - (
                    number_of_merged_frame_views / number_of_views_with_mergeable_frames
                )
            except ZeroDivisionError:
                urgency = 0.0
        return MergedFrameViewSuggester.spawn(
            parent_id, bubble_chamber, targets, urgency
        )

    def _passes_preliminary_checks(self):
        possible_views = self.bubble_chamber.views.filter(
            lambda x: x.parent_frame.parent_concept
            == self.bubble_chamber.concepts["conjunction"]
            and x.unhappiness < self.FLOATING_POINT_TOLERANCE
        )
        possible_frames = self.bubble_chamber.frames.filter(
            lambda x: x.parent_frame is None
            and x.parent_concept == self.bubble_chamber.concepts["conjunction"]
            and not x.is_sub_frame
            and x.exigency > 0
        )
        possible_target_combos = [
            self.bubble_chamber.new_dict(
                {"view": view, "frame": frame},
            )
            for view in possible_views
            for frame in possible_frames
            if view.parent_frame.progenitor.relations.filter(
                lambda x: x.parent_concept == self.bubble_chamber.concepts["more"]
                and x.conceptual_space == self.bubble_chamber.spaces["grammar"]
                and (
                    (frame == x.start and view.parent_frame.progenitor == x.end)
                    or (view.parent_frame.progenitor == x.start and frame == x.end)
                )
            ).not_empty
        ]
        try:
            targets = self.bubble_chamber.random_machine.select(
                possible_target_combos,
                key=lambda x: fuzzy.AND(x["view"].activation, x["frame"].exigency),
            )
            self.targets["view"] = targets["view"]
            self.targets["frame"] = targets["frame"]
            self.targets["contextual_space"] = self.targets["view"].input_spaces.get()
        except MissingStructureError:
            return False
        return True
