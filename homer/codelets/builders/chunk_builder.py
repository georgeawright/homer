from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Node
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
            slot = Node(
                structure_id=ID.new(Node),
                parent_id=self.codelet_id,
                locations=[Location([None], self.target_space)],
                parent_space=self.target_space,
                quality=0.0,
                links_in=StructureCollection(),
                links_out=StructureCollection(),
            )
            locations = self.target_node.locations
            left_branch, right_branch = (
                (StructureCollection({self.target_node}), None)
                if self.target_branch == "left"
                else (None, StructureCollection({self.target_node}))
            )
            chunk = Chunk(
                structure_id=ID.new(Chunk),
                parent_id=self.codelet_id,
                locations=locations,
                members=StructureCollection({self.target_node, slot}),
                parent_space=self.target_space,
                quality=0.0,
                left_branch=left_branch,
                right_branch=right_branch,
                rule=self.target_rule,
            )
            chunk.free_branch.add(slot)
            self.child_structures = StructureCollection({slot, chunk})
        if self.target_slot is not None and self.target_slot_filler is not None:
            self.target_root.members.add(self.target_slot_filler)
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
