from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Link, Space


class Relation(Link):
    def __init__(
        self,
        start: Structure,
        end: Structure,
        parent_concept: Concept,
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
    ):
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
