from __future__ import annotations
from typing import List, Set, Tuple

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunks import View
from homer.structures.links import Correspondence
from homer.structures.spaces import WorkingSpace


class ViewBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_view = target_view
        self.second_target_view = None
        self.correspondences = None
        self.correspondences_to_add = None
        self.child_structure = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_view,
            urgency,
        )

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target = bubble_chamber.views.get_exigent()
        return cls.spawn(parent_id, bubble_chamber, target, target.unhappiness)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        try:
            self.second_target_view = self.target_view.nearby().get_random()
        except MissingStructureError:
            return False
        return not self.bubble_chamber.has_view(
            StructureCollection.union(
                self.target_view.members, self.second_target_view.members
            )
        )

    def _calculate_confidence(self):
        self.confidence = 1.0
        self.correspondences = self.target_view.members.copy()
        self.correspondences_to_add = self.second_target_view.members.copy()
        while not self.correspondences_to_add.is_empty():
            correspondence = self.correspondences_to_add.get_random()
            self._add_correspondence_and_update_confidence(correspondence)

    def _add_correspondence_and_update_confidence(self, new: Correspondence):
        final_compatibility = 1.0
        final_required_correspondences = {new}
        for old in self.target_view.members:
            (
                compatibility,
                required_correspondences,
            ) = self._compatibility_and_required_correspondences(old, new)
            if compatibility < final_compatibility:
                final_compatibility = compatibility
            final_required_correspondences |= required_correspondences
        if final_compatibility < self.confidence:
            self.confidence = final_compatibility
        self._transfer_correspondences(*final_required_correspondences)

    def _compatibility_and_required_correspondences(
        self, old: Correspondence, new: Correspondence
    ) -> Tuple[float, Set[Correspondence]]:
        common_arguments = old.common_arguments_with(new)
        if len(common_arguments) == 0:
            compatibility = min(old.quality, new.quality)
            # you are only as strong as your weakest link
            return (compatibility, set())
        if len(common_arguments) == 1:
            third_correspondence_start = (
                old.start if old.start not in common_arguments else old.end
            )
            third_correspondence_end = (
                new.end if new.end not in common_arguments else new.start
            )
            try:
                third_correspondence = self.second_target_view.members.where(
                    start=third_correspondence_start, end=third_correspondence_end
                ).get_random()
            except MissingStructureError:
                return (0, set())
            compatibility = min(old.quality, new.quality, third_correspondence.quality)
            return (compatibility, {third_correspondence})
        # 2 common arguments => the correspondences are equivalent/competing
        return (0, set())

    def _transfer_correspondences(self, *correspondences: List[Correspondence]):
        for correspondence in correspondences:
            self.correspondences.add(correspondence)
            self.correspondences_to_add.remove(correspondence)

    def _process_structure(self):
        view_id = ID.new(View)
        top_level_working_space = self.bubble_chamber.spaces["top level working"]
        view_output_space = WorkingSpace(
            ID.new(WorkingSpace),
            self.codelet_id,
            f"output for {view_id}",
            self.bubble_chamber.concepts["text"],
            self.bubble_chamber.conceptual_spaces["text"],
            [Location([], top_level_working_space)],
            StructureCollection(),
            1,
            [],
            [],
        )
        self.bubble_chamber.working_spaces.add(view_output_space)
        self.bubble_chamber.logger.log(view_output_space)
        view = View(
            view_id,
            self.codelet_id,
            Location([], top_level_working_space),
            self.correspondences,
            view_output_space,
            0,
        )
        self.bubble_chamber.views.add(view)
        self.bubble_chamber.logger.log(view)
        self.child_structure = view

    def _engender_follow_up(self):
        from homer.codelets.evaluators import ViewEvaluator

        self.child_codelets.append(
            ViewEvaluator.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.child_structure,
                self.confidence,
            )
        )

    def _fizzle(self):
        self.child_codelets.append(self.make(self.codelet_id, self.bubble_chamber))

    def _fail(self):
        self.child_codelets.append(self.make(self.codelet_id, self.bubble_chamber))
