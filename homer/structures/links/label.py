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
        parent_concept: Concept,
        locations: List[Location],
        quality: FloatBetweenOneAndZero,
    ):
        Link.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            start=start,
            end=None,
            locations=locations,
            parent_concept=parent_concept,
            quality=quality,
            links_in=None,
            links_out=None,
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
        start = kwargs["start"] if "start" in kwargs else self.start
        parent_space = (
            kwargs["parent_space"] if "parent_space" in kwargs else self.parent_space
        )
        new_locations = [
            location
            for location in self.locations
            if location.space.is_conceptual_space
        ]
        new_locations.append(Location(self.location.coordinates, parent_space))
        parent_id = kwargs["parent_id"] if "parent_id" in kwargs else ""
        new_label = Label(
            structure_id=ID.new(Label),
            parent_id=parent_id,
            start=start,
            parent_concept=self.parent_concept,
            locations=new_locations,
            quality=self.quality,
        )
        return new_label

    def nearby(self, space: Space = None) -> StructureCollection:
        nearby_chunks = self.start.nearby(self.parent_space)
        return StructureCollection.difference(
            StructureCollection.union(
                StructureCollection(
                    {label for chunk in nearby_chunks for label in chunk.labels}
                ),
                self.start.labels,
            ),
            StructureCollection({self}),
        )
