from __future__ import annotations

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
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
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        is_bidirectional: bool = True,
    ):
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

    @property
    def parent_space(self) -> Space:
        return self._parent_space

    def copy(self, **kwargs) -> Relation:
        """Takes keyword arguments 'start', 'end', 'parent_space', and 'parent_id'."""
        start = kwargs["start"] if "start" in kwargs else self.start
        end = kwargs["end"] if "end" in kwargs else self.end
        parent_space = (
            kwargs["parent_space"] if "parent_space" in kwargs else self.parent_space
        )
        parent_id = kwargs["parent_id"] if "parent_id" in kwargs else ""
        new_relation = Relation(
            ID.new(Relation),
            parent_id,
            start,
            end,
            self.parent_concept,
            parent_space,
            self.quality,
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
