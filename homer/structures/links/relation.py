from __future__ import annotations
from typing import List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
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
        end: Structure,
        arguments: StructureCollection,
        parent_concept: Concept,
        conceptual_space: ConceptualSpace,
        locations: List[Location],
        quality: FloatBetweenOneAndZero,
        parent_space: Space,
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
            end=end,
            arguments=arguments,
            locations=locations,
            parent_concept=parent_concept,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
        )
        self._parent_space = parent_space
        self.conceptual_space = conceptual_space
        self.is_relation = True
        self.is_bidirectional = is_bidirectional

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "parent_id": self.parent_id,
            "parent_concept": self.parent_concept.structure_id
            if self.parent_concept is not None
            else None,
            "parent_concept_name": self.parent_concept.name
            if self.parent_concept is not None
            else None,
            "conceptual_space": self.conceptual_space.structure_id
            if self.conceptual_space is not None
            else None,
            "conceptual_space_name": self.conceptual_space.name
            if self.conceptual_space is not None
            else None,
            "start": self.start.structure_id,
            "end": self.end.structure_id,
            "locations": [str(location) for location in self.locations],
            "parent_space": self.parent_space.structure_id
            if self.parent_space is not None
            else None,
            "quality": self.quality,
            "activation": self.activation,
        }

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
            location.copy()
            for location in self.locations
            if location.space.is_conceptual_space
        ]
        if parent_space is not None:
            new_locations.append(
                TwoPointLocation(
                    start.location_in_space(start.parent_space).coordinates,
                    end.location_in_space(end.parent_space).coordinates,
                    parent_space,
                )
            )
        parent_id = kwargs["parent_id"] if "parent_id" in kwargs else ""
        return bubble_chamber.new_relation(
            parent_id=parent_id,
            start=start,
            end=end,
            parent_concept=self.parent_concept,
            conceptual_space=self.conceptual_space,
            locations=new_locations,
            quality=self.quality,
            parent_space=self.parent_space,
        )

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
