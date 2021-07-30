from __future__ import annotations

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
        self._target_structures = target_structures
        self.target_space = None
        self.target_rule = None
        self.target_root = None
        self.target_node = None
        self.target_slot = None
        self.target_slot_filler = None
        self.target_branch = None

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

    def _passes_preliminary_checks(self):
        self.target_space = self._target_structures["target_space"]
        self.target_rule = self._target_structures["target_rule"]
        self.target_root = self._target_structures["target_root"]
        self.target_node = self._target_structures["target_node"]
        self.target_slot = self._target_structures["target_slot"]
        self.target_slot_filler = self._target_structures["target_slot_filler"]
        self.target_branch = self._target_structures["target_branch"]
        suggested_members = StructureCollection.union(
            self.target_root.members.where(is_slot=False)
            if self.target_root is not None
            else StructureCollection(),
            StructureCollection({self.target_node}),
            StructureCollection({self.target_slot_filler})
            if self.target_slot_filler is not None
            else StructureCollection(),
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
                    Location([[None]], space)
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
                    Location([[None]], space)
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
            slot = Chunk(
                structure_id=ID.new(Chunk),
                parent_id=self.codelet_id,
                locations=slot_locations,
                members=StructureCollection(),
                parent_space=self.target_space,
                quality=0.0,
                left_branch=None,
                right_branch=None,
                rule=None,
            )
            left_branch, right_branch = (
                (StructureCollection({self.target_node}), None)
                if self.target_branch == "left"
                else (None, StructureCollection({self.target_node}))
            )
            chunk = Chunk(
                structure_id=ID.new(Chunk),
                parent_id=self.codelet_id,
                locations=chunk_locations,
                members=StructureCollection({self.target_node}),
                parent_space=self.target_space,
                quality=0.0,
                left_branch=left_branch,
                right_branch=right_branch,
                rule=self.target_rule,
            )
            self.child_structures = StructureCollection({chunk})
            self.target_node.super_chunks.add(chunk)
            slot.super_chunks.add(chunk)
            if chunk.has_free_branch:
                chunk.free_branch.add(slot)
                chunk.members.add(slot)
                self.child_structures.add(slot)
        if self.target_slot is not None and self.target_slot_filler is not None:
            self.target_root.members.add(self.target_slot_filler)
            self.target_slot_filler.super_chunks.add(self.target_root)
            self.child_structures = StructureCollection(
                {self.target_root, self.target_slot}
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
