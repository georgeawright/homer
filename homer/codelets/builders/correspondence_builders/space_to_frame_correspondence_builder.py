from homer.codelets.builders import CorrespondenceBuilder


class SpaceToFrameCorrespondenceBuilder(CorrespondenceBuilder):
    # TODO: test
    def _process_structure(self):
        if (
            self.target_structure_two.is_link
            and not self.target_structure_two.parent_concept.is_filled_in
        ):
            self.bubble_chamber.new_relation(
                parent_id=self.codelet_id,
                start=self.target_structure_two.parent_concept,
                end=self.target_structure_one.parent_concept,
                parent_concept=None,
                locations=[],
                quality=1.0,
            )
        correspondence = self.bubble_chamber.new_correspondence(
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
        self.child_structures = self.bubble_chamber.new_structure_collection(
            correspondence
        )
