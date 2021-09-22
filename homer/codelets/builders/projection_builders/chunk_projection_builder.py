from homer.id import ID
from homer.location import Location
from homer.codelets.builders import ProjectionBuilder
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence


class ChunkProjectionBuilder(ProjectionBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.projection_evaluators import (
            ChunkProjectionEvaluator,
        )

        return ChunkProjectionEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _process_structure(self):
        output_location = Location(
            self.target_projectee.location.coordinates,
            self.target_view.output_space,
        )
        chunk = self.target_projectee.copy_to_location(
            output_location, parent_id=self.codelet_id
        )
        self.target_view.output_space.add(chunk)
        self.bubble_chamber.chunks.add(chunk)
        for location in chunk.locations:
            self.bubble_chamber.logger.log(location.space)
        self.bubble_chamber.logger.log(chunk)
        frame_to_output_correspondence = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            start=self.target_projectee,
            end=chunk,
            locations=[self.target_projectee.location, chunk.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
            parent_view=self.target_view,
            quality=0.0,
        )
        self.child_structures = StructureCollection(
            {chunk, frame_to_output_correspondence}
        )
        self.bubble_chamber.correspondences.add(frame_to_output_correspondence)
        self.bubble_chamber.logger.log(frame_to_output_correspondence)
        self.target_view.members.add(frame_to_output_correspondence)
        self.target_projectee.links_in.add(frame_to_output_correspondence)
        self.target_projectee.links_out.add(frame_to_output_correspondence)
        chunk.links_in.add(frame_to_output_correspondence)
        chunk.links_out.add(frame_to_output_correspondence)
        for location in frame_to_output_correspondence.locations:
            location.space.add(frame_to_output_correspondence)
        if self.target_projectee.is_slot:
            non_frame_to_output_correspondence = Correspondence(
                ID.new(Correspondence),
                self.codelet_id,
                start=self.non_frame_correspondee,
                end=chunk,
                locations=[
                    self.non_frame_correspondee.location_in_space(self.non_frame),
                    chunk.location,
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
            chunk.links_in.add(non_frame_to_output_correspondence)
            chunk.links_out.add(non_frame_to_output_correspondence)
            self.non_frame_correspondee.links_in.add(non_frame_to_output_correspondence)
            self.non_frame_correspondee.links_out.add(
                non_frame_to_output_correspondence
            )
            self.bubble_chamber.logger.log(non_frame_to_output_correspondence)
            for location in non_frame_to_output_correspondence.locations:
                location.space.add(non_frame_to_output_correspondence)
        self.bubble_chamber.logger.log(self.target_view)
