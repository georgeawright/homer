from linguoplotter.codelets.builders import CorrespondenceBuilder


class SpaceToFrameCorrespondenceBuilder(CorrespondenceBuilder):
    def _process_structure(self):
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
            and self.targets["end"].parent_concept.is_slot
            and not self.targets["end"].parent_concept.is_filled_in
        ):
            self.targets["end"].parent_concept._non_slot_value = self.targets[
                "start"
            ].parent_concept
        correspondence = self.bubble_chamber.new_correspondence(
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
        self._structure_concept.instances.add(correspondence)
        self.child_structures.add(correspondence)
        self.bubble_chamber.loggers["structure"].log_view(self.targets["view"])
