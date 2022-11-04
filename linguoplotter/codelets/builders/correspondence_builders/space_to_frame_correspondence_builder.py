from linguoplotter.codelets.builders import CorrespondenceBuilder


class SpaceToFrameCorrespondenceBuilder(CorrespondenceBuilder):
    def _process_structure(self):
        self.child_structures = self.bubble_chamber.new_structure_collection()
        if (
            self.target_conceptual_space is not None
            and self.target_conceptual_space.is_slot
        ):
            if self.target_structure_two.is_label:
                self.target_view.parent_frame.specify_space(
                    self.target_conceptual_space,
                    self.target_structure_one.parent_concept.parent_space,
                )
            if self.target_structure_two.is_relation:
                self.target_view.parent_frame.specify_space(
                    self.target_conceptual_space,
                    self.target_structure_one.conceptual_space,
                )
        if (
            self.target_structure_two.is_link
            and self.target_structure_two.parent_concept.is_slot
            and not self.target_structure_two.parent_concept.is_filled_in
        ):
            self.target_structure_two.parent_concept._non_slot_value = (
                self.target_structure_one.parent_concept
            )
        #            for relative in self.target_structure_two.parent_concept.relatives:
        #                if self.target_view.parent_frame.input_space.contents.where(
        #                    is_link=True, parent_concept=relative
        #                ).is_empty():
        #                    relation_with_relative = (
        #                        self.target_structure_two.parent_concept.relations_with(
        #                            relative
        #                        ).get()
        #                    )
        #                    structure_two_parent_relatives = (
        #                        self.target_structure_two.parent_concept.non_slot_value.relatives
        #                    )
        #                    relative._non_slot_value = structure_two_parent_relatives.filter(
        #                        lambda x: x in relative.parent_space.contents
        #                        and x.has_relation_with(
        #                            self.target_structure_two.parent_concept.non_slot_value,
        #                            relation_with_relative.parent_concept.non_slot_value,
        #                        )
        #                    ).get()
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
        self._structure_concept.instances.add(correspondence)
        self.child_structures.add(correspondence)
        self.bubble_chamber.loggers["structure"].log_view(self.target_view)
