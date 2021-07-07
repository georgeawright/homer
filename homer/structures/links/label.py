from __future__ import annotations

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
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
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
    ):
        end = None
        Link.__init__(
            self,
            structure_id,
            parent_id,
            start,
            end,
            [start.location_in_space(parent_space)] if parent_space is not None else [],
            parent_concept,
            quality,
            links_in=None,
            links_out=None,
        )
        self._parent_space = parent_space
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
    def parent_space(self) -> Space:
        return self._parent_space

    @property
    def is_slot(self) -> bool:
        return self.parent_concept is None

    def copy(self, **kwargs: dict) -> Label:
        """Takes keyword arguments 'start', 'end', 'parent_space', and 'parent_id'."""
        start = kwargs["start"] if "start" in kwargs else self.start
        parent_space = (
            kwargs["parent_space"] if "parent_space" in kwargs else self.parent_space
        )
        parent_id = kwargs["parent_id"] if "parent_id" in kwargs else ""
        new_label = Label(
            ID.new(Label),
            parent_id,
            start,
            self.parent_concept,
            parent_space,
            self.quality,
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
