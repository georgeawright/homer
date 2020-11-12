from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Link, Space
from homer.structures.spaces import ConceptualSpace, WorkingSpace


class Correspondence(Link):
    def __init__(
        self,
        start: Structure,
        end: Structure,
        start_space: Space,
        end_space: Space,
        parent_concept: Concept,
        parent_space: WorkingSpace,
        conceptual_space: ConceptualSpace,
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
        self.start_space = start_space
        self.end_space = end_space
        self.conceptual_space = conceptual_space

    def nearby(self):
        return StructureCollection.difference(
            StructureCollection.union(
                self.start.correspondences,
                self.end.correspondences,
                self.parent_space.contents,
            ),
            StructureCollection({self}),
        )

    def get_slot_argument(self):
        from homer.structures.chunks import Slot

        if isinstance(self.start, Slot):
            return self.start
        if isinstance(self.end, Slot):
            return self.end
        raise Exception("Correspondence has no slot argument")

    def get_non_slot_argument(self):
        from homer.structures.chunks import Slot

        if not isinstance(self.start, Slot):
            return self.start
        if not isinstance(self.end, Slot):
            return self.end
        raise Exception("Correspondence has no non slot argument")
