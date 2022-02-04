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
        frames: StructureCollection,
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
        self.frames = frames
        self.input_spaces = input_spaces
        self.output_space = output_space
        self.members = members
        self.node_groups = []
        self.grouped_nodes = {}
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
        return self.parent_frame.slots

    def copy(self, **kwargs: dict):
        raise NotImplementedError

    def add(self, correspondence: "Correspondence"):
        self.members.add(correspondence)
        for node_pair in correspondence.node_pairs:
            if all(node in self.grouped_nodes for node in node_pair):
                continue
            for node_group in self.node_groups:
                if (
                    node_group.get(node_pair[0].parent_space) == node_pair[0]
                    or node_group.get(node_pair[1].parent_space) == node_pair[1]
                ):
                    node_group[node_pair[0].parent_space] = node_pair[0]
                    node_group[node_pair[1].parent_space] = node_pair[1]
                    self.grouped_nodes[node_pair[0]] = True
                    self.grouped_nodes[node_pair[1]] = True
            if node_pair[0] not in self.grouped_nodes:
                self.node_groups.append(
                    {
                        node_pair[0].parent_space: node_pair[0],
                        node_pair[1].parent_space: node_pair[1],
                    }
                )
                self.grouped_nodes[node_pair[0]] = True
                self.grouped_nodes[node_pair[1]] = True

    def has_member(
        self,
        parent_concept: Concept,
        conceptual_space: Space,
        start: Structure,
        end: Structure,
    ) -> bool:
        return not self.members.where(
            parent_concept=parent_concept,
            conceptual_space=conceptual_space,
            start=start,
            end=end,
        ).is_empty()

    def can_accept_member(
        self,
        parent_concept: Concept,
        conceptual_space: Space,
        start: Structure,
        end: Structure,
    ) -> bool:
        if self.has_member(parent_concept, conceptual_space, start, end):
            return False
        if not end.correspondences.filter(lambda x: x in self.members).is_empty():
            return False
        potential_node_groups = (
            [{start.parent_space: start, end.parent_space: end}]
            if start.is_node
            else [
                {
                    start.start.parent_space: start.start,
                    end.start.parent_space: end.start,
                }
            ]
            if start.is_label
            else [
                {
                    start.start.parent_space: start.start,
                    end.start.parent_space: end.start,
                },
                {
                    start.end.parent_space: start.end,
                    end.end.parent_space: end.end,
                },
            ]
        )
        for existing_node_group in self.node_groups:
            for potential_group in potential_node_groups:
                if all(
                    node in existing_node_group.values()
                    for node in potential_group.values()
                ):
                    return True
                if all(space in existing_node_group for space in potential_group):
                    if any(
                        node in existing_node_group.values()
                        for node in potential_group.values()
                    ):
                        return False
        return True

    def __repr__(self) -> str:
        inputs = ", ".join([space.structure_id for space in self.input_spaces])
        return (
            f"<{self.structure_id} "
            + f"from {inputs} to {self.output_space.structure_id} "
            + f"with {self.parent_frame} ({self.parent_frame.parent_concept.name})>"
        )
