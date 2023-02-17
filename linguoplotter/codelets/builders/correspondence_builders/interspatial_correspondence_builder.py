from linguoplotter.codelets.builders import CorrespondenceBuilder
from linguoplotter.structure_collections import StructureSet


class InterspatialCorrespondenceBuilder(CorrespondenceBuilder):
    def _passes_preliminary_checks(self):
        if (
            self.targets["start_sub_view"].super_views.not_empty
            and self.targets["view"] not in self.targets["start_sub_view"].super_views
        ):
            self.bubble_chamber.loggers["activity"].log_set(
                self.targets["start_sub_view"].super_views, "super views"
            )
            return False
        if (
            self.targets["end_sub_view"] is not None
            and self.targets["end_sub_view"].super_views.not_empty
            and self.targets["view"] not in self.targets["end_sub_view"].super_views
        ):
            self.bubble_chamber.loggers["activity"].log_set(
                self.targets["end_sub_view"].super_views, "super views"
            )
            return False
        try:
            matched_start_sub_frame = self.targets["view"].matched_secondary_sub_frames[
                self.targets["start_sub_frame"]
            ]
            if matched_start_sub_frame != self.targets["start_sub_view"].parent_frame:
                self.bubble_chamber.loggers["activity"].log_set(
                    self.targets["view"].matched_secondary_sub_frames,
                    "matched sub frames",
                )
                return False
        except KeyError:
            pass
        if self.targets["end"].is_relation:
            try:
                matched_end_sub_frame = self.targets[
                    "view"
                ].matched_secondary_sub_frames[self.targets["end_sub_frame"]]
                if matched_end_sub_frame != self.targets["end_sub_view"].parent_frame:
                    self.bubble_chamber.loggers["activity"].log_set(
                        self.targets["view"].matched_secondary_sub_frames,
                        "matched sub frames",
                    )
                    return False
            except KeyError:
                pass
        if self.targets["start_sub_view"] not in self.targets["view"].sub_views:
            for correspondence in self.targets["start_sub_view"].members:
                if not self.targets["view"].can_accept_member(
                    correspondence.parent_concept,
                    correspondence.conceptual_space,
                    correspondence.start,
                    correspondence.end,
                    sub_view=self.targets["start_sub_view"],
                ):
                    self.bubble_chamber.loggers["activity"].log(
                        repr(self.targets["view"]) + f" cannot accept {correspondence}"
                    )
                    return False
        if (
            self.targets["end_sub_view"] is not None
            and self.targets["end_sub_view"] not in self.targets["view"].sub_views
        ):
            for correspondence in self.targets["end_sub_view"].members:
                if not self.targets["view"].can_accept_member(
                    correspondence.parent_concept,
                    correspondence.conceptual_space,
                    correspondence.start,
                    correspondence.end,
                    sub_view=self.targets["end_sub_view"],
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
        )

    def _process_structure(self):
        if self.targets["end"].is_relation:
            self.targets["view"].frames = StructureSet.union(
                self.targets["view"].frames,
                self.targets["start_sub_view"].frames,
                self.targets["end_sub_view"].frames,
            )
            self.targets["view"].matched_secondary_sub_frames[
                self.targets["start_sub_frame"]
            ] = self.targets["start_sub_view"].parent_frame
            self.targets["view"].matched_secondary_sub_frames[
                self.targets["end_sub_frame"]
            ] = self.targets["end_sub_view"].parent_frame
            for (
                matched_sub_frame,
                matching_sub_frame,
            ) in self.targets["start_sub_view"].matched_secondary_sub_frames.items():
                self.targets["view"].matched_secondary_sub_frames[
                    matched_sub_frame
                ] = matching_sub_frame
            for (
                matched_sub_frame,
                matching_sub_frame,
            ) in self.targets["end_sub_view"].matched_secondary_sub_frames.items():
                self.targets["view"].matched_secondary_sub_frames[
                    matched_sub_frame
                ] = matching_sub_frame
            for correspondence in self.targets["start_sub_view"].members:
                self.targets["view"].add(correspondence)
            for correspondence in self.targets["end_sub_view"].members:
                self.targets["view"].add(correspondence)
            self.targets["view"].sub_views.add(self.targets["start_sub_view"])
            self.targets["start_sub_view"].super_views.add(self.targets["view"])
            self.targets["view"].sub_views.add(self.targets["end_sub_view"])
            self.targets["end_sub_view"].super_views.add(self.targets["view"])
            if self.targets["space"] is not None and self.targets["space"].is_slot:
                self.targets["view"].specify_space(
                    self.targets["space"],
                    self.targets["start"].conceptual_space,
                )
                self.targets["space"] = self.targets["start"].conceptual_space
            if (
                self.targets["end"].parent_concept.is_slot
                and not self.targets["end"].parent_concept.is_filled_in
            ):
                self.targets["end"].parent_concept._non_slot_value = self.targets[
                    "start"
                ].parent_concept
            correspondence = self.bubble_chamber.new_correspondence(
                parent_id=self.codelet_id,
                start=self.targets["start"],
                end=self.targets["end"],
                locations=[],
                parent_concept=self.targets["concept"],
                conceptual_space=self.targets["space"],
                parent_view=self.targets["view"],
            )
        elif self.targets["end"].is_label:
            self.targets["view"].frames = StructureSet.union(
                self.targets["view"].frames,
                self.targets["start_sub_view"].frames,
            )
            self.targets["view"].matched_secondary_sub_frames[
                self.targets["start_sub_frame"]
            ] = self.targets["start_sub_view"].parent_frame
            for (
                matched_sub_frame,
                matching_sub_frame,
            ) in self.targets["start_sub_view"].matched_secondary_sub_frames.items():
                self.targets["view"].matched_secondary_sub_frames[
                    matched_sub_frame
                ] = matching_sub_frame
            for correspondence in self.targets["start_sub_view"].members:
                self.targets["view"].add(correspondence)
            self.targets["view"].sub_views.add(self.targets["start_sub_view"])
            self.targets["start_sub_view"].super_views.add(self.targets["view"])
            if self.targets["space"] is not None and self.targets["space"].is_slot:
                self.targets["view"].specify_space(
                    self.targets["space"],
                    self.targets["start"]
                    .parent_spaces.where(is_conceptual_space=True)
                    .get(),
                )
                self.targets["space"] = (
                    self.targets["start"]
                    .parent_spaces.where(is_conceptual_space=True)
                    .get()
                )
            if (
                self.targets["end"].parent_concept.is_slot
                and not self.targets["end"].parent_concept.is_filled_in
            ):
                self.targets["end"].parent_concept._non_slot_value = self.targets[
                    "start"
                ].parent_concept
            if (
                any(
                    [
                        link.correspondences.not_empty
                        for link in self.targets["start"].start.links.where(
                            is_interspatial=True
                        )
                    ]
                )
                and self.targets["end"].start not in self.targets["view"].grouped_nodes
            ):
                node_group = [
                    group
                    for group in self.targets["view"].node_groups
                    if self.targets["start"].start in group.values()
                ][0]
                old_end_start = self.targets["end"].start
                new_end_start = node_group[self.targets["end"].start.parent_space]
                for link in old_end_start.links_out:
                    link.start = new_end_start
                    new_end_start.links_out.add(link)
                for link in old_end_start.links_in:
                    link.end = new_end_start
                    new_end_start.links_in.add(link)
                for relation in new_end_start.relations.copy():
                    while (
                        len(
                            new_end_start.relations.where(
                                start=relation.start,
                                end=relation.end,
                                parent_concept=relation.parent_concept,
                                conceptual_space=relation.conceptual_space,
                            )
                        )
                        > 1
                    ):
                        relation_to_remove = new_end_start.relations.where(
                            start=relation.start,
                            end=relation.end,
                            parent_concept=relation.parent_concept,
                            conceptual_space=relation.conceptual_space,
                        ).get()
                        relation_to_remove.start.links_out.remove(relation_to_remove)
                        relation_to_remove.end.links_in.remove(relation_to_remove)
                        self.targets["frame"].interspatial_links.remove(
                            relation_to_remove
                        )
                for space in old_end_start.parent_spaces:
                    space.contents.remove(old_end_start)
            correspondence = self.bubble_chamber.new_correspondence(
                parent_id=self.codelet_id,
                start=self.targets["start"],
                end=self.targets["end"],
                locations=[],
                parent_concept=self.targets["concept"],
                conceptual_space=self.targets["space"],
                parent_view=self.targets["view"],
            )
        self._structure_concept.instances.add(correspondence)
        self.child_structures.add(correspondence)
