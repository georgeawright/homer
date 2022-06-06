from linguoplotter.codelets.builders import CorrespondenceBuilder
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection import StructureCollection


class PotentialSubFrameToFrameCorrespondenceBuilder(CorrespondenceBuilder):
    def _passes_preliminary_checks(self):
        if not self.target_sub_view.super_views.is_empty():
            self.bubble_chamber.loggers["activity"].log_collection(
                self, self.target_sub_view.super_views, "super views"
            )
            return False
        if self.sub_frame in self.target_view.matched_sub_frames:
            self.bubble_chamber.loggers["activity"].log_collection(
                self, self.target_view.matched_sub_frames, "matched sub frames"
            )
            return False
        for correspondence in self.target_sub_view.members:
            if not self.target_view.can_accept_member(
                correspondence.parent_concept,
                correspondence.conceptual_space,
                correspondence.start,
                correspondence.end,
            ):
                self.bubble_chamber.loggers["activity"].log(
                    self, f"{self.target_view} cannot accept {correspondence}"
                )
                return False
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
                self.bubble_chamber.loggers["activity"].log(
                    self,
                    f"{self.target_view} cannot accept correspondence to "
                    + f"{target_structure_zero}",
                )
                return False
        except MissingStructureError:
            pass
        return self.target_view.can_accept_member(
            self.parent_concept,
            self.target_conceptual_space,
            self.target_structure_one,
            self.target_structure_two,
        )

    def _process_structure(self):
        self.child_structures = self.bubble_chamber.new_structure_collection()
        self.target_view.frames = StructureCollection.union(
            self.target_view.frames, self.target_sub_view.frames
        )
        self.target_view.matched_sub_frames[
            self.sub_frame
        ] = self.target_sub_view.parent_frame
        for (
            matched_sub_frame,
            matching_sub_frame,
        ) in self.target_sub_view.matched_sub_frames.items():
            self.target_view.matched_sub_frames[matched_sub_frame] = matching_sub_frame
        for correspondence in self.target_sub_view.members:
            self.bubble_chamber.loggers["activity"].log_collection(
                self, self.target_view.node_groups, "Target_view node groups"
            )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Adding {correspondence} to {self.target_view}"
            )
            self.target_view.add(correspondence)
            self.bubble_chamber.loggers["activity"].log_collection(
                self, self.target_view.node_groups, "Target_view node groups"
            )
        self.target_view.sub_views.add(self.target_sub_view)
        self.target_sub_view.super_views.add(self.target_view)
        if (
            self.target_structure_two.is_link
            and not self.target_structure_two.parent_concept.is_filled_in
        ):
            self.target_structure_two.parent_concept._non_slot_value = (
                self.target_structure_one.parent_concept
            )
        sub_frame_correspondence = self.bubble_chamber.new_correspondence(
            parent_id=self.codelet_id,
            start=self.target_structure_one,
            end=self.target_structure_two,
            locations=[
                self.target_structure_one.location_in_space(self.target_space_one),
                self.target_structure_two.location_in_space(self.target_space_two),
            ],
            parent_concept=self.parent_concept,
            conceptual_space=self.target_conceptual_space,
            parent_view=self.target_view,
        )
        self.child_structures.add(sub_frame_correspondence)
        self._structure_concept.instances.add(sub_frame_correspondence)
        self._add_contextual_space_correspondence()
        self.bubble_chamber.loggers["structure"].log_view(self.target_view)
