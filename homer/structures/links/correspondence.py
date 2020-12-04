from __future__ import annotations

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Link, Space
from homer.structures.spaces import ConceptualSpace, WorkingSpace


class Correspondence(Link):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
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
        self.start_space = start_space
        self.end_space = end_space
        self.conceptual_space = conceptual_space

    def copy(
        self, old_arg: Structure = None, new_arg: Structure = None, parent_id: str = ""
    ) -> Correspondence:
        start = new_arg if new_arg is not None and old_arg == self.start else self.start
        end = new_arg if new_arg is not None and old_arg == self.end else self.end
        new_correspondence = Correspondence(
            ID.new(Correspondence),
            parent_id,
            start,
            end,
            self.start_space,
            self.end_space,
            self.parent_concept,
            self.parent_space,
            self.conceptual_space,
            self.quality,
        )
        return new_correspondence

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

    def common_arguments_with(self, other: Correspondence):
        return StructureCollection(
            set.intersection({self.start, self.end}, {other.start, other.end})
        )
