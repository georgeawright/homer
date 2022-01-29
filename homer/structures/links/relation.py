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
from homer.structures.spaces import ConceptualSpace


class Relation(Link):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        start: Structure,
        arguments: StructureCollection,
        parent_concept: Concept,
        conceptual_space: ConceptualSpace,
        locations: List[Location],
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        is_bidirectional: bool = True,
    ):
        Link.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            start=start,
            arguments=arguments,
            locations=locations,
            parent_concept=parent_concept,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
        )
        self.conceptual_space = conceptual_space
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
        bubble_chamber = kwargs["bubble_chamber"]
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
                start.location_in_space(start.parent_space).coordinates,
                end.location_in_space(end.parent_space).coordinates,
                parent_space,
            )
        )
        parent_id = kwargs["parent_id"] if "parent_id" in kwargs else ""
        new_relation = Relation(
            structure_id=ID.new(Relation),
            parent_id=parent_id,
            start=start,
            arguments=bubble_chamber.new_structure_collection(start, end),
            parent_concept=self.parent_concept,
            conceptual_space=self.conceptual_space,
            locations=new_locations,
            quality=self.quality,
            links_in=bubble_chamber.new_structure_collection(),
            links_out=bubble_chamber.new_structure_collection(),
            parent_spaces=bubble_chamber.new_structure_collection(
                *[location.space for location in new_locations]
            ),
        )
        return new_relation

    def nearby(self, space: Space = None) -> StructureCollection:
        return (
            StructureCollection.intersection(
                self.start.relations,
                self.end.relations,
            )
            .filter(lambda x: x.parent_spaces == self.parent_spaces)
            .excluding(self)
        )

    def __repr__(self) -> str:
        concept = "none" if self.parent_concept is None else self.parent_concept.name
        conceptual_space = (
            "" if self.conceptual_space is None else self.conceptual_space.name
        )
        args = ", ".join([arg.structure_id for arg in self.arguments])
        spaces = ", ".join([location.space.name for location in self.locations])
        return f"<{self.structure_id} {concept}-{conceptual_space}({args}) in {spaces}>"
