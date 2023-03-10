from linguoplotter.codelets.builders import ProjectionBuilder


class RelationProjectionBuilder(ProjectionBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators.projection_evaluators import (
            RelationProjectionEvaluator,
        )

        return RelationProjectionEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

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
        end_correspondence = (
            self.targets["projectee"]
            .end.correspondences_to_space(self.targets["view"].output_space)
            .get()
        )
        corresponding_end = end_correspondence.end
        conceptual_location = self.targets["projectee"].location_in_space(
            parent_concept.parent_space
        )
        output_location = corresponding_start.location_in_space(
            self.targets["view"].output_space
        )
        locations = [conceptual_location, output_location]
        relation = self.bubble_chamber.new_relation(
            parent_id=self.codelet_id,
            start=corresponding_start,
            end=corresponding_end,
            parent_concept=parent_concept,
            locations=locations,
            quality=0.0,
        )
        frame_to_output_correspondence = self.bubble_chamber.new_correspondence(
            parent_id=self.codelet_id,
            start=self.targets["projectee"],
            end=relation,
            locations=[self.targets["projectee"].location, relation.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
            parent_view=self.targets["view"],
            quality=0.0,
            is_projection=True,
        )
        self.child_structures.add(relation)
        self.child_structures.add(frame_to_output_correspondence)
