from __future__ import annotations
import random

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation, chunking_exigency
from homer.structures.nodes import Rule

# TODO: chunking exigency needs to depend on rule - high level grammar rules, sameness, have low exigency


class ChunkSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.target_space = None
        self.target_rule = None
        self.target_root = None
        self.target_node = None
        self.target_slot = None
        self.target_slot_filler = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders import ChunkBuilder

        return ChunkBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        qualifier = (
            "TopDown" if target_structures["target_rule"] is not None else "BottomUp"
        )
        codelet_id = ID.new(cls, qualifier)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.production_views.get(key=activation)
        target_space = target_view.spaces.where_not(is_frame=True).get()
        target_node = target_space.contents.where(is_node=True).get(
            key=chunking_exigency
        )
        urgency = urgency if urgency is not None else target_node.unchunkedness
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_space": target_space,
                "target_node": target_node,
                "target_rule": None,
            },
            urgency,
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_rule: Rule,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.production_views.get(key=activation)
        target_space = target_view.spaces.where_not(is_frame=True).get()
        target_node = StructureCollection(
            {
                node
                for node in target_space.contents.where(is_node=True)
                if target_rule.is_compatible_with(node)
            }
        ).get(key=chunking_exigency)
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_space": target_space,
                "target_node": target_node,
                "target_rule": target_rule,
            },
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self):
        self.target_space = self._target_structures["target_space"]
        self.target_rule = self._target_structures["target_rule"]
        self.target_node = self._target_structures["target_node"]
        if self.target_rule is None:
            try:
                self.target_root = self.target_node.super_chunks.get()
                self.target_rule = self.target_root.rule
            except MissingStructureError:
                self.target_root = None
                self.target_rule = self.bubble_chamber.rules.where(
                    instance_type=type(self.target_node)
                ).get(key=activation)
        else:
            try:
                self.target_root = StructureCollection(
                    {
                        chunk
                        for chunk in self.target_node.super_chunks
                        if chunk.rule == self.target_rule
                    }
                ).get()
            except MissingStructureError:
                self.target_root = None
        if self.target_root is not None:
            try:
                self.target_slot = self.target_root.members.where(is_slot=True).get()
                if (
                    self.target_slot.location_in_space(self.target_space).coordinates
                    == []
                ):
                    self.target_slot_filler = (
                        self.target_root.nearby()
                        .where(is_slot=False)
                        .get(key=chunking_exigency)
                    )
                else:
                    self.target_slot_filler = (
                        self.target_space.contents.where(is_node=True, is_slot=False)
                        .at(self.target_slot.location)
                        .get(key=chunking_exigency)
                    )
            except MissingStructureError:
                return False
        self._target_structures["target_rule"] = self.target_rule
        self._target_structures["target_root"] = self.target_root
        self._target_structures["target_slot"] = self.target_slot
        self._target_structures["target_slot_filler"] = self.target_slot_filler
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

    def _calculate_confidence(self):
        def randomized_compatibility(compatibility, randomness, satisfaction):
            return compatibility * (
                compatibility * satisfaction + randomness * (1 - satisfaction)
            )

        left_randomness = random.random()
        right_randomness = random.random()
        child = (
            self.target_node
            if self.target_slot_filler is None
            else self.target_slot_filler
        )
        left_compatibility = self.target_rule.compatibility_with(
            root=self.target_root, child=child, branch="left"
        )
        right_compatibility = self.target_rule.compatibility_with(
            root=self.target_root, child=child, branch="right"
        )
        left_probability = randomized_compatibility(
            left_compatibility, left_randomness, self.bubble_chamber.satisfaction
        )
        right_probability = randomized_compatibility(
            right_compatibility, right_randomness, self.bubble_chamber.satisfaction
        )
        if left_probability > right_probability:
            self._target_structures["target_branch"] = "left"
            self.confidence = left_compatibility
        else:
            self._target_structures["target_branch"] = "right"
            self.confidence = right_compatibility

    def _fizzle(self):
        pass
