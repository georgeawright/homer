from __future__ import annotations
from typing import List

from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.locations import TwoPointLocation
from linguoplotter.structure import Structure
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures import Link, Space
from linguoplotter.structures.nodes import Concept


class Label(Link):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        start: Structure,
        arguments: StructureSet,
        parent_concept: Concept,
        locations: List[Location],
        quality: FloatBetweenOneAndZero,
        parent_space: Space,
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
    ):
        Link.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            start=start,
            end=None,
            arguments=arguments,
            locations=locations,
            parent_concept=parent_concept,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self._parent_space = parent_space
        self.is_label = True

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
            "start": self.start.structure_id,
            "locations": [str(location) for location in self.locations],
            "parent_space": self.parent_space.structure_id,
            "quality": self.quality,
            "activation": self.activation,
        }

    @classmethod
    def get_builder_class(cls):
        from linguoplotter.codelets.builders import LabelBuilder

        return LabelBuilder

    @classmethod
    def get_evaluator_class(cls):
        from linguoplotter.codelets.evaluators import LabelEvaluator

        return LabelEvaluator

    @classmethod
    def get_selector_class(cls):
        from linguoplotter.codelets.selectors import LabelSelector

        return LabelSelector

    def copy(self, **kwargs: dict) -> Label:
        """Takes keyword arguments 'start', 'end', 'parent_space', and 'parent_id'."""
        bubble_chamber = kwargs["bubble_chamber"]
        start = kwargs["start"] if "start" in kwargs else self.start
        parent_space = (
            kwargs["parent_space"] if "parent_space" in kwargs else self.parent_space
        )
        new_locations = [
            location.copy()
            for location in self.locations
            if location.space.is_conceptual_space
        ]
        try:
            new_locations.append(Location(self.location.coordinates, parent_space))
        except NotImplementedError:
            new_locations.append(
                TwoPointLocation(
                    self.location.start_coordinates,
                    self.location.end_coordinates,
                    parent_space,
                )
            )
        parent_id = kwargs["parent_id"] if "parent_id" in kwargs else ""
        return bubble_chamber.new_label(
            parent_id=parent_id,
            start=start,
            parent_concept=self.parent_concept,
            locations=new_locations,
            quality=self.quality,
            parent_space=parent_space,
        )

    def nearby(self, space: Space = None) -> StructureSet:
        return self.start.labels.filter(
            lambda x: x.parent_spaces == self.parent_spaces
        ).excluding(self)
