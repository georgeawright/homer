from linguoplotter.codelets.builders import ProjectionBuilder


class LabelProjectionBuilder(ProjectionBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators.projection_evaluators import (
            LabelProjectionEvaluator,
        )

        return LabelProjectionEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _process_structure(self):
        parent_concept = (
            self.targets["projectee"].parent_concept
            if not self.targets["projectee"].is_slot
            else self.targets["projectee"].parent_concept.non_slot_value
        )
        start_correspondence = (
            self.targets["projectee"]
            .start.correspondences_to_space(self.targets["view"].output_space)
            .get()
        )
        corresponding_start = start_correspondence.end
        conceptual_location = self.targets["projectee"].location_in_space(
            parent_concept.parent_space
        )
        output_location = corresponding_start.location_in_space(
            self.targets["view"].output_space
        )
        locations = [conceptual_location, output_location]
        label = self.bubble_chamber.new_label(
            parent_id=self.codelet_id,
            start=corresponding_start,
            parent_concept=parent_concept,
            locations=locations,
            quality=0.0,
        )
        frame_to_output_correspondence = self.bubble_chamber.new_correspondence(
            parent_id=self.codelet_id,
            start=self.targets["projectee"],
            end=label,
            locations=[self.targets["projectee"].location, label.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
            parent_view=self.targets["view"],
            quality=0.0,
        )
        self.child_structures.add(label)
        self.child_structures.add(frame_to_output_correspondence)
        self.bubble_chamber.loggers["structure"].log_view(self.targets["view"])
