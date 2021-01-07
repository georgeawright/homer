from __future__ import annotations

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Link, Space


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
    ):
        Link.__init__(
            self,
            structure_id,
            parent_id,
            start,
            end,
            start.location_in_space(parent_space) if parent_space is not None else None,
            parent_concept,
            quality,
            links_in=None,
            links_out=None,
        )

    def copy(
        self, old_arg: Structure = None, new_arg: Structure = None, parent_id: str = ""
    ) -> Relation:
        start = new_arg if new_arg is not None and old_arg == self.start else self.start
        end = new_arg if new_arg is not None and old_arg == self.end else self.end
        new_relation = Relation(
            ID.new(Relation),
            parent_id,
            start,
            end,
            self.parent_concept,
            self.parent_space,
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
