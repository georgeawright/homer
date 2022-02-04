from homer.codelets.builders import CorrespondenceBuilder


class SubFrameToFrameCorrespondenceBuilder(CorrespondenceBuilder):
    def _process_structure(self):
        self.child_structures = self.bubble_chamber.new_structure_collection()
        if (
            self.target_structure_two.is_link
            and not self.target_structure_two.parent_concept.is_filled_in
        ):
            if self.target_structure_one.parent_concept.is_slot:
                slot_value = (
                    self.target_structure_one.parent_concept.relations.filter(
                        lambda x: not x.end.is_slot
                    )
                    .get()
                    .end
                )
            else:
                slot_value = self.target_structure_one.parent_concept
            concept_link = self.bubble_chamber.new_relation(
                parent_id=self.codelet_id,
                start=self.target_structure_two.parent_concept,
                end=slot_value,
                parent_concept=None,
                locations=[],
                quality=1.0,
            )
            self.child_structures.add(concept_link)
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
        self._add_contextual_space_correspondence()
