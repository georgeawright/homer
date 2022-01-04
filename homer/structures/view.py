import operator
from typing import List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Frame
from homer.structures.nodes import Concept
from homer.structures.space import Space
from homer.structures.spaces import ContextualSpace


class View(Structure):
    """A collection of spaces and self-consistent correspondences between them."""

    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        parent_frame: Frame,
        locations: List[Location],
        members: StructureCollection,
        input_spaces: StructureCollection,
        output_space: ContextualSpace,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            locations=locations,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
        )
        self.parent_frame = parent_frame
        self.value = None
        self.input_spaces = input_spaces
        self.output_space = output_space
        self.members = members
        self.input_node_pairs = []
        self.slot_values = {}
        self.is_view = True

    @property
    def raw_input_space(self) -> Space:
        return self.input_spaces.filter(
            lambda x: x.parent_concept.name == "input"
        ).get()

    @property
    def input_contextual_spaces(self):
        return self.input_spaces.where(is_contextual_space=True)

    @property
    def size(self):
        return len(self.members)

    @property
    def slots(self):
        return StructureCollection.union(*[frame.slots for frame in self.input_frames])

    def copy(self, **kwargs: dict):
        raise NotImplementedError

    def add(self, correspondence: "Correspondence"):
        self.members.add(correspondence)
        for node_pair in correspondence.node_pairs:
            if node_pair not in self.input_node_pairs:
                self.input_node_pairs.append(node_pair)

    def has_member(
        self,
        parent_concept: Concept,
        start: Structure,
        end: Structure,
        start_space: Space,
        end_space: Space,
    ) -> bool:
        for correspondence in self.members:
            if (
                correspondence.parent_concept == parent_concept
                and correspondence.start == start
                and correspondence.end == end
                and correspondence.start_space == start_space
                and correspondence.end_space == end_space
            ):
                return True
        return False

    def can_accept_member(self, correspondence: "Correspondence") -> bool:
        # TODO: first check that target view does not have member
        if not StructureCollection.intersection(
            self.members, correspondence.end.correspondences
        ).is_empty():
            return False
        potential_node_pairs = correspondence.node_pairs
        if all(
            potential_node_pair in self.input_node_pairs
            for potential_node_pair in potential_node_pairs
        ):
            return True
        return not any(
            operator.xor(
                potential_node_pair[0] == existing_node_pair[0],
                potential_node_pair[1] == existing_node_pair[1],
            )
            for potential_node_pair in potential_node_pairs
            for existing_node_pair in self.input_node_pairs
        )

    def __repr__(self) -> str:
        inputs = ", ".join([space.structure_id for space in self.input_spaces])
        return (
            f"<{self.structure_id} from {inputs} to {self.output_space.structure_id}>"
        )
