from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Link, Space


class Label(Link):
    def __init__(
        self,
        start: Structure,
        parent_concept: Concept,
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
    ):
        end = None
        Link.__init__(
            self,
            start,
            end,
            parent_concept,
            parent_space,
            quality,
            links_in=None,
            links_out=None,
        )

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
