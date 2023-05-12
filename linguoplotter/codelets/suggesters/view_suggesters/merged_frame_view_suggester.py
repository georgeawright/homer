from linguoplotter import fuzzy
from linguoplotter.codelets.suggesters import BottomUpCohesionViewSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collections import StructureSet


class MergedFrameViewSuggester(BottomUpCohesionViewSuggester):
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
            and x.relations_with(self.targets["view"].parent_frame.progenitor).not_empty
        )
        possible_target_combos = [
            self.bubble_chamber.new_dict(
                {"view": view, "frame": frame},
            )
            for view in possible_views
            for frame in possible_frames
            if StructureSet.intersection(view.parent_frame.relations, frame.relations)
            .where(parent_concept=self.bubble_chamber.concepts["more"])
            .not_empty
        ]
        try:
            targets = self.bubble_chamber.random_machine.select(
                possible_target_combos,
                key=lambda x: fuzzy.AND(x["view"].activation, x["frame"].exigency),
            )
            self.targets["view"] = targets["view"]
            self.targets["frame"] = targets["frame"]
        except MissingStructureError:
            return False
        return True
