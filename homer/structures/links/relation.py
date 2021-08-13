from __future__ import annotations
from typing import List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.locations import TwoPointLocation
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Link, Space
from homer.structures.nodes import Concept


class Relation(Link):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        start: Structure,
        end: Structure,
        parent_concept: Concept,
        locations: List[Location],
        quality: FloatBetweenOneAndZero,
        is_bidirectional: bool = True,
    ):
        Link.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            start=start,
            end=end,
            locations=locations,
            parent_concept=parent_concept,
            quality=quality,
            links_in=None,
            links_out=None,
        )
        self.is_relation = True
        self.is_bidirectional = is_bidirectional

    @classmethod
    def get_builder_class(cls):
        from homer.codelets.builders import RelationBuilder

        return RelationBuilder

    @classmethod
    def get_evaluator_class(cls):
        from homer.codelets.evaluators import RelationEvaluator

        return RelationEvaluator

    @classmethod
    def get_selector_class(cls):
        from homer.codelets.selectors import RelationSelector

        return RelationSelector

    def copy(self, **kwargs) -> Relation:
        """Takes keyword arguments 'start', 'end', 'parent_space', and 'parent_id'."""
        start = kwargs["start"] if "start" in kwargs else self.start
        end = kwargs["end"] if "end" in kwargs else self.end
        parent_space = (
            kwargs["parent_space"] if "parent_space" in kwargs else self.parent_space
        )
        new_locations = [
            location
            for location in self.locations
            if location.space.is_conceptual_space
        ]
        new_locations.append(
            TwoPointLocation(
                self.location.start_coordinates,
                self.location.end_coordinates,
                parent_space,
            )
        )
        parent_id = kwargs["parent_id"] if "parent_id" in kwargs else ""
        new_relation = Relation(
            structure_id=ID.new(Relation),
            parent_id=parent_id,
            start=start,
            end=end,
            parent_concept=self.parent_concept,
            locations=new_locations,
            quality=self.quality,
        )
        return new_relation

    def nearby(self, space: Space = None) -> StructureCollection:
        nearby_chunks = StructureCollection.union(
            self.start.nearby(self.parent_space),
            self.end.nearby(self.parent_space),
        )
        return StructureCollection.difference(
            StructureCollection.union(
                StructureCollection(
                    {
                        relation
                        for chunk in nearby_chunks
                        for relation in chunk.relations
                    }
                ),
                self.start.relations,
                self.end.relations,
            ),
            StructureCollection({self}),
        )
