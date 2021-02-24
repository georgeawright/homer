from __future__ import annotations

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Link, Space
from homer.structures.nodes import Concept
from homer.structures.spaces import ConceptualSpace
from homer.tools import equivalent_space


class Correspondence(Link):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        start: Structure,
        end: Structure,
        location: Location,
        start_space: Space,
        end_space: Space,
        parent_concept: Concept,
        conceptual_space: ConceptualSpace,
        quality: FloatBetweenOneAndZero,
        is_privileged: bool = False,
    ):
        Link.__init__(
            self,
            structure_id,
            parent_id,
            start,
            end,
            location,
            parent_concept,
            quality,
            links_in=None,
            links_out=None,
        )
        self.start_space = start_space
        self.end_space = end_space
        self.conceptual_space = conceptual_space
        self.is_privileged = is_privileged

    def copy(
        self, old_arg: Structure = None, new_arg: Structure = None, parent_id: str = ""
    ) -> Correspondence:
        start = new_arg if new_arg is not None and old_arg == self.start else self.start
        end = new_arg if new_arg is not None and old_arg == self.end else self.end
        start_space = equivalent_space(start, self.start_space)
        end_space = equivalent_space(end, self.end_space)
        if self.location == self.start.location:
            new_location = start.location
        else:
            new_location = Location.for_correspondence_between(
                start.location_in_space(start_space),
                end.location_in_space(end_space),
                self.location.space,
            )
        new_correspondence = Correspondence(
            ID.new(Correspondence),
            parent_id,
            start,
            end,
            new_location,
            start_space,
            end_space,
            self.parent_concept,
            self.conceptual_space,
            self.quality,
            is_privileged=self.is_privileged,
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
        if self.start.is_slot:
            return self.start
        if self.end.is_slot:
            return self.end
        raise Exception("Correspondence has no slot argument")

    def get_non_slot_argument(self):
        if not self.start.is_slot:
            return self.start
        if not self.end.is_slot:
            return self.end
        raise Exception("Correspondence has no non slot argument")

    def common_arguments_with(self, other: Correspondence):
        return StructureCollection(
            set.intersection({self.start, self.end}, {other.start, other.end})
        )
