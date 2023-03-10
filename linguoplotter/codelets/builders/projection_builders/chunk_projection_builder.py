from linguoplotter.location import Location
from linguoplotter.codelets.builders import ProjectionBuilder


class ChunkProjectionBuilder(ProjectionBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators.projection_evaluators import (
            ChunkProjectionEvaluator,
        )

        return ChunkProjectionEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self) -> bool:
        return not self.targets["projectee"].has_correspondence_to_space(
            self.targets["view"].output_space
        )

    def _process_structure(self):
        output_location = Location(
            self.targets["projectee"].location.coordinates,
            self.targets["view"].output_space,
        )
        chunk = self.targets["projectee"].copy_to_location(
            output_location, self.bubble_chamber, parent_id=self.codelet_id
        )
        self.targets["view"].output_space.add(chunk)
        self.bubble_chamber.chunks.add(chunk)
        for location in chunk.locations:
            self.bubble_chamber.loggers["structure"].log(location.space)
        self.bubble_chamber.loggers["structure"].log(chunk)
        frame_to_output_correspondence = self.bubble_chamber.new_correspondence(
            parent_id=self.codelet_id,
            start=self.targets["projectee"],
            end=chunk,
            locations=[self.targets["projectee"].location, chunk.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
            parent_view=self.targets["view"],
            quality=0.0,
            is_projection=True,
        )
        self.child_structures.add(chunk)
        self.child_structures.add(frame_to_output_correspondence)
