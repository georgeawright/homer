from linguoplotter.codelets.builders import CorrespondenceBuilder


class SubFrameToFrameCorrespondenceBuilder(CorrespondenceBuilder):
    def _process_structure(self):
        self.child_structures = self.bubble_chamber.new_structure_collection()
        if self.target_structure_two.is_link and self.target_conceptual_space.is_slot:
            self.target_view.parent_frame.specify_space(
                self.target_conceptual_space,
                self.target_structure_one.parent_concept.parent_space,
            )
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
        self.bubble_chamber.loggers["structure"].log_view(self.target_view)
