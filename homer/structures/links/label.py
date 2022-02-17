from __future__ import annotations
from typing import List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Link, Space
from homer.structures.nodes import Concept


class Label(Link):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        start: Structure,
        arguments: StructureCollection,
        parent_concept: Concept,
        locations: List[Location],
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
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
        self.is_label = True

    @classmethod
    def get_builder_class(cls):
        from homer.codelets.builders import LabelBuilder

        return LabelBuilder

    @classmethod
    def get_evaluator_class(cls):
        from homer.codelets.evaluators import LabelEvaluator

        return LabelEvaluator

    @classmethod
    def get_selector_class(cls):
        from homer.codelets.selectors import LabelSelector

        return LabelSelector

    @property
    def is_slot(self) -> bool:
        return self.parent_concept is None

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
        new_locations.append(Location(self.location.coordinates, parent_space))
        parent_id = kwargs["parent_id"] if "parent_id" in kwargs else ""
        new_label = Label(
            structure_id=ID.new(Label),
            parent_id=parent_id,
            start=start,
            arguments=bubble_chamber.new_structure_collection(start),
            parent_concept=self.parent_concept,
            locations=new_locations,
            quality=self.quality,
            links_in=bubble_chamber.new_structure_collection(),
            links_out=bubble_chamber.new_structure_collection(),
            parent_spaces=bubble_chamber.new_structure_collection(
                *[location.space for location in new_locations]
            ),
        )
        start.links_out.add(new_label)
        for space in new_label.parent_spaces:
            space.add(new_label)
        return new_label

    def nearby(self, space: Space = None) -> StructureCollection:
        return self.start.labels.filter(
            lambda x: x.parent_spaces == self.parent_spaces
        ).excluding(self)
