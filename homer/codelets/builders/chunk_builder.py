from __future__ import annotations
import math

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Chunk


class ChunkBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: StructureCollection,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_space = target_structures.get("target_space")
        self.target_rule = target_structures.get("target_rule")
        self.target_root = target_structures.get("target_root")
        self.target_node = target_structures.get("target_node")
        self.target_slot = target_structures.get("target_slot")
        self.target_slot_filler = target_structures.get("target_slot_filler")
        self.target_branch = target_structures.get("target_branch")

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators import ChunkEvaluator

        return ChunkEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_chunk: Chunk,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_chunk,
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    @property
    def targets_dict(self):
        return {
            "target_space": self.target_space,
            "target_rule": self.target_rule,
            "target_root": self.target_root,
            "target_node": self.target_node,
            "target_slot": self.target_slot,
            "target_slot_filler": self.target_slot_filler,
            "target_branch": self.target_branch,
        }

    def _passes_preliminary_checks(self):
        suggested_members = StructureCollection.union(
            self.target_root.members.where(is_slot=False)
            if self.target_root is not None
            else self.bubble_chamber.new_structure_collection(),
            self.bubble_chamber.new_structure_collection(self.target_node),
            self.bubble_chamber.new_structure_collection(self.target_slot_filler)
            if self.target_slot_filler is not None
            else self.bubble_chamber.new_structure_collection(),
        )
        for chunk in self.bubble_chamber.chunks:
            if (
                chunk.rule == self.target_rule
                and chunk.members.where(is_slot=False) == suggested_members
            ):
                return False
        return True

    def _process_structure(self):
        if self.target_root is None:
            if (
                self.target_rule.right_concept is None
                and self.target_rule.root_concept == self.target_rule.left_concept
            ):
                slot_locations = [Location([], self.target_space)] + [
                    Location([[math.nan for _ in range(space.no_of_dimensions)]], space)
                    for space in self.target_space.conceptual_spaces
                ]
                chunk_locations = self.target_node.locations
            elif self.target_rule.right_concept is None:
                root_location = self.target_node.location_in_space(self.target_space)
                root_conceptual_location = (
                    self.target_rule.root_concept.location_in_space(
                        self.target_rule.parent_space
                    )
                )
                slot_locations = []
                chunk_locations = [root_location, root_conceptual_location]
            else:
                target_node_location = self.target_node.location_in_space(
                    self.target_space
                )
                adjacent_location = (
                    target_node_location.get_adjacent_location_right()
                    if self.target_branch == "left"
                    else target_node_location.get_adjacent_location_left()
                )
                slot_conceptual_locations = [
                    Location([[math.nan]], space)
                    for space in self.target_space.conceptual_spaces
                ]
                root_location = (
                    Location.merge(
                        self.target_node.location_in_space(self.target_space),
                        adjacent_location,
                    )
                    if self.target_branch == "left"
                    else Location.merge(
                        adjacent_location,
                        self.target_node.location_in_space(self.target_space),
                    )
                )
                root_conceptual_location = (
                    self.target_rule.root_concept.location_in_space(
                        self.target_rule.parent_space
                    )
                )
                slot_locations = [adjacent_location] + slot_conceptual_locations
                chunk_locations = [root_location, root_conceptual_location]
            slot = self.bubble_chamber.new_chunk(
                parent_id=self.codelet_id,
                locations=slot_locations,
                members=self.bubble_chamber.new_structure_collection(),
                parent_space=self.target_space,
                quality=0.0,
                left_branch=self.bubble_chamber.new_structure_collection(),
                right_branch=self.bubble_chamber.new_structure_collection(),
                rule=None,
            )
            if self.target_branch == "left":
                left_branch = self.bubble_chamber.new_structure_collection(
                    self.target_node
                )
                right_branch = self.bubble_chamber.new_structure_collection()
            else:
                left_branch = self.bubble_chamber.new_structure_collection()
                right_branch = self.bubble_chamber.new_structure_collection(
                    self.target_node
                )
            chunk = self.bubble_chamber.new_chunk(
                parent_id=self.codelet_id,
                locations=chunk_locations,
                members=self.bubble_chamber.new_structure_collection(self.target_node),
                parent_space=self.target_space,
                quality=0.0,
                left_branch=left_branch,
                right_branch=right_branch,
                rule=self.target_rule,
            )
            self.child_structures = self.bubble_chamber.new_structure_collection(chunk)
            if chunk.has_free_branch:
                chunk.free_branch.add(slot)
                chunk.members.add(slot)
                slot.super_chunks.add(chunk)
                self.child_structures.add(slot)
        if self.target_slot is not None and self.target_slot_filler is not None:
            self.target_root.members.add(self.target_slot_filler)
            self.target_slot_filler.super_chunks.add(self.target_root)
            self.child_structures = self.bubble_chamber.new_structure_collection(
                self.target_root, self.target_slot
            )
            for location in self.target_root.locations:
                location.coordinates.append(
                    self.target_slot_filler.location_in_space(location.space)
                )
            if self.target_branch == "left":
                self.target_root.left_branch.add(self.target_slot_filler)
            if self.target_branch == "right":
                self.target_root.right_branch.add(self.target_slot_filler)
            if not self.target_root.has_free_branch:
                self.target_root.members.remove(self.target_slot)
                self.target_space.contents.remove(self.target_slot)
                self.child_structures.remove(self.target_slot)

    def _fizzle(self):
        pass

    def _fail(self):
        pass
