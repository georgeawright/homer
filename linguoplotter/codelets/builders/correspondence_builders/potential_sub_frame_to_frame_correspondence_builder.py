from linguoplotter.codelets.builders import CorrespondenceBuilder
from linguoplotter.structure_collections import StructureSet


class PotentialSubFrameToFrameCorrespondenceBuilder(CorrespondenceBuilder):
    def _passes_preliminary_checks(self):
        if self.targets["sub_view"].super_views.not_empty:
            self.bubble_chamber.loggers["activity"].log_set(
                self.targets["sub_view"].super_views, "super views"
            )
            return False
        if self.targets["sub_frame"] in self.targets["view"].matched_sub_frames:
            self.bubble_chamber.loggers["activity"].log_set(
                self.targets["view"].matched_sub_frames, "matched sub frames"
            )
            return False
        if self.targets["sub_view"].parent_frame.parent_concept.location_in_space(
            self.bubble_chamber.spaces["grammar"]
        ) == self.bubble_chamber.concepts["sentence"].location_in_space(
            self.bubble_chamber.spaces["grammar"]
        ):
            if self.targets["sub_view"].unhappiness > self.FLOATING_POINT_TOLERANCE:
                return False
            if any(
                [
                    self.targets["sub_view"].raw_input_nodes == v.raw_input_nodes
                    for v in self.targets["view"].sub_views
                ]
            ):
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
                    repr(self.targets["view"]) + f" cannot accept {correspondence}"
                )
                return False
        return self.targets["view"].can_accept_member(
            self.targets["concept"],
            self.targets["space"],
            self.targets["start"],
            self.targets["end"],
            sub_view=self.targets["sub_view"],
        )

    def _process_structure(self):
        self.targets["view"].frames = StructureSet.union(
            self.targets["view"].frames, self.targets["sub_view"].frames
        )
        self.targets["view"].matched_sub_frames[
            self.targets["sub_frame"]
        ] = self.targets["sub_view"].parent_frame
        for (
            matched_sub_frame,
            matching_sub_frame,
        ) in self.targets["sub_view"].matched_sub_frames.items():
            self.targets["view"].matched_sub_frames[
                matched_sub_frame
            ] = matching_sub_frame
        for correspondence in self.targets["sub_view"].members:
            self.targets["view"].add(correspondence)
        self.targets["view"].sub_views.add(self.targets["sub_view"])
        self.targets["sub_view"].super_views.add(self.targets["view"])
        if self.targets["space"] is not None and self.targets["space"].is_slot:
            if self.targets["end"].is_label:
                self.targets["view"].specify_space(
                    self.targets["space"],
                    self.targets["start"].parent_concept.parent_space,
                )
                self.targets["space"] = self.targets[
                    "start"
                ].parent_concept.parent_space
            if self.targets["end"].is_relation:
                self.targets["view"].specify_space(
                    self.targets["space"],
                    self.targets["start"].conceptual_space,
                )
                self.targets["space"] = self.targets["start"].conceptual_space
        if (
            self.targets["end"].is_link
            and not self.targets["end"].parent_concept.is_filled_in
        ):
            start_concept = self.targets["start"].parent_concept
            end_concept = self.targets["end"].parent_concept
            end_concept._non_slot_value = start_concept
        sub_frame_correspondence = self.bubble_chamber.new_correspondence(
            parent_id=self.codelet_id,
            start=self.targets["start"],
            end=self.targets["end"],
            locations=[
                self.targets["start"].parent_space_location,
                self.targets["end"].parent_space_location,
            ],
            parent_concept=self.targets["concept"],
            conceptual_space=self.targets["space"],
            parent_view=self.targets["view"],
        )
        self.child_structures.add(sub_frame_correspondence)
        self._structure_concept.instances.add(sub_frame_correspondence)
