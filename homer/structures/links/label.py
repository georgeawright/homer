from __future__ import annotations

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Link, Space


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
            parent_concept,
            parent_space,
            quality,
            links_in=None,
            links_out=None,
        )

    def copy(
        self, old_arg: Structure = None, new_arg: Structure = None, parent_id: str = ""
    ) -> Label:
        start = new_arg if new_arg is not None else self.start
        new_label = Label(
            ID.new(Label),
            parent_id,
            start,
            self.parent_concept,
            self.parent_space,
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
