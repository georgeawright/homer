from linguoplotter.codelets.builders import RelationBuilder
from linguoplotter.location import Location
from linguoplotter.locations import TwoPointLocation
from linguoplotter.tools import centroid_difference


class InterspatialRelationBuilder(RelationBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators.relation_evaluators import (
            InterspatialRelationEvaluator,
        )

        return InterspatialRelationEvaluator

    def _process_structure(self):
        if self.child_structures.not_empty:
            self.bubble_chamber.loggers["activity"].log(
                "Equivalent relation already exists"
            )
            return
        start_coordinates = (
            self.targets["start"].location_in_space(self.targets["space"]).coordinates
        )
        end_coordinates = (
            self.targets["end"].location_in_space(self.targets["space"]).coordinates
        )
        location_coordinates = (
            centroid_difference(start_coordinates, end_coordinates)
            if start_coordinates != [] and end_coordinates != []
            else []
        )
        locations = [
            Location([[location_coordinates]], self.targets["concept"].parent_space),
            TwoPointLocation(start_coordinates, end_coordinates, self.targets["space"]),
            Location([], self.targets["start"].parent_space),
            Location([], self.targets["end"].parent_space),
        ]
        relation = self.bubble_chamber.new_relation(
            parent_id=self.codelet_id,
            start=self.targets["start"],
            end=self.targets["end"],
            locations=locations,
            parent_concept=self.targets["concept"],
            parent_space=None,
            conceptual_space=self.targets["space"],
            quality=0,
            is_interspatial=True,
        )
        self._structure_concept.instances.add(relation)
        self.child_structures.add(relation)
        if self.targets["concept"].is_reversible:
            if (
                self.targets["start"]
                .relations.where(
                    start=self.targets["end"],
                    parent_concept=self.targets["concept"].reverse,
                    conceptual_space=self.targets["space"],
                )
                .is_empty
            ):
                mirror_relation = self.bubble_chamber.new_relation(
                    parent_id=self.codelet_id,
                    start=self.targets["end"],
                    end=self.targets["start"],
                    locations=locations,
                    parent_concept=self.targets["concept"].reverse,
                    parent_space=None,
                    conceptual_space=self.targets["space"],
                    quality=0,
                    is_interspatial=True,
                )
                self._structure_concept.instances.add(mirror_relation)
                self.child_structures.add(mirror_relation)
        self._structure_concept.recalculate_salience()
