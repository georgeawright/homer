from homer.id import ID
from homer.codelets.builders import ProjectionBuilder
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label


class LabelProjectionBuilder(ProjectionBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.projection_evaluators import (
            LabelProjectionEvaluator,
        )

        return LabelProjectionEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _process_structure(self):
        start_correspondence = self.target_projectee.start.correspondences_to_space(
            self.target_view.output_space
        ).get()
        corresponding_start = start_correspondence.end
        parent_concept = self.target_view.slot_values[
            self.frame_correspondee.structure_id
        ]
        conceptual_location = self.target_projectee.location_in_space(
            parent_concept.parent_space
        )
        output_location = corresponding_start.location_in_space(
            self.target_view.output_space
        )
        locations = [conceptual_location, output_location]
        label = Label(
            ID.new(Label),
            self.codelet_id,
            corresponding_start,
            parent_concept,
            locations,
            0.0,
        )
        start_correspondence.links_out.add(label)
        self.bubble_chamber.labels.add(label)
        for location in locations:
            location.space.add(label)
            self.bubble_chamber.logger.log(location.space)
        self.bubble_chamber.logger.log(label)
        frame_to_output_correspondence = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            start=self.target_projectee,
            end=label,
            locations=[self.target_projectee.location, label.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
            parent_view=self.target_view,
            quality=0.0,
        )
        self.child_structures = StructureCollection(
            {label, frame_to_output_correspondence}
        )
        self.bubble_chamber.correspondences.add(frame_to_output_correspondence)
        self.bubble_chamber.logger.log(frame_to_output_correspondence)
        self.target_view.members.add(frame_to_output_correspondence)
        self.target_projectee.links_in.add(frame_to_output_correspondence)
        self.target_projectee.links_out.add(frame_to_output_correspondence)
        label.links_in.add(frame_to_output_correspondence)
        label.links_out.add(frame_to_output_correspondence)
        for location in frame_to_output_correspondence.locations:
            location.space.add(frame_to_output_correspondence)
        if self.target_projectee.is_slot:
            non_frame_to_output_correspondence = Correspondence(
                ID.new(Correspondence),
                self.codelet_id,
                start=self.non_frame_correspondee,
                end=label,
                locations=[
                    self.non_frame_correspondee.location_in_space(self.non_frame),
                    label.location,
                ],
                parent_concept=self.bubble_chamber.concepts["same"],
                conceptual_space=self.target_correspondence.conceptual_space,
                parent_view=self.target_view,
                quality=0.0,
            )
            self.child_structures.add(non_frame_to_output_correspondence)
            self.bubble_chamber.correspondences.add(non_frame_to_output_correspondence)
            self.bubble_chamber.logger.log(non_frame_to_output_correspondence)
            self.target_view.members.add(non_frame_to_output_correspondence)
            label.links_in.add(non_frame_to_output_correspondence)
            label.links_out.add(non_frame_to_output_correspondence)
            self.non_frame_correspondee.links_in.add(non_frame_to_output_correspondence)
            self.non_frame_correspondee.links_out.add(
                non_frame_to_output_correspondence
            )
            self.bubble_chamber.logger.log(non_frame_to_output_correspondence)
            for location in non_frame_to_output_correspondence.locations:
                location.space.add(non_frame_to_output_correspondence)
        self.bubble_chamber.logger.log(self.target_view)
