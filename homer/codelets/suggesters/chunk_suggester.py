from __future__ import annotations

from homer import fuzzy
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
        self.target_space = target_structures.get("target_space")
        self.target_rule = target_structures.get("target_rule")
        self.target_root = target_structures.get("target_root")
        self.target_node = target_structures.get("target_node")
        self.target_slot = target_structures.get("target_slot")
        self.target_slot_filler = target_structures.get("target_slot_filler")
        self.target_branch = target_structures.get("target_branch")

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
        target_space = target_view.input_spaces.get()
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
        target_space = target_view.input_spaces.get()
        target_node = bubble_chamber.new_structure_collection(
            *[
                node
                for node in target_space.contents.where(is_node=True)
                if target_rule.is_compatible_with(node)
            ]
        ).get(key=chunking_exigency)
        urgency = target_node.chunking_exigency if urgency is None else urgency
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
        if self.target_rule is None:
            try:
                self.target_root = self.target_node.super_chunks.get()
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found target_root: {self.target_root}"
                )
                self.target_rule = self.target_root.rule
            except MissingStructureError:
                self.target_root = None
                self.target_rule = self.bubble_chamber.rules.where(
                    instance_type=type(self.target_node)
                ).get()
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found target_rule: {self.target_rule}"
            )
        else:
            try:
                self.target_root = self.target_node.super_chunks.where(
                    rule=self.target_rule
                ).get()
            except MissingStructureError:
                self.target_root = None
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found target_root: {self.target_root}"
            )
        if self.target_root is not None:
            try:
                self.target_slot = self.target_root.members.where(is_slot=True).get()
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found target_slot: {self.target_slot}"
                )
                if (
                    self.target_slot.location_in_space(self.target_space).coordinates
                    == []
                ):
                    self.target_slot_filler = (
                        self.target_root.nearby()
                        .where(is_slot=False)
                        .filter(lambda x: x not in self.target_root.members)
                        .get(key=chunking_exigency)
                    )
                else:
                    self.target_slot_filler = (
                        self.target_space.contents.where(is_node=True, is_slot=False)
                        .at(self.target_slot.location)
                        .get(key=chunking_exigency)
                    )
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found target_slot_filler: {self.target_slot_filler}"
                )
            except MissingStructureError:
                return False
        suggested_members = StructureCollection.union(
            self.target_root.members.where(is_slot=False)
            if self.target_root is not None
            else self.bubble_chamber.new_structure_collection(),
            self.bubble_chamber.new_structure_collection(self.target_node),
            self.bubble_chamber.new_structure_collection(self.target_slot_filler)
            if self.target_slot_filler is not None
            else self.bubble_chamber.new_structure_collection(),
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self, suggested_members, "Suggested members"
        )
        return self.bubble_chamber.chunks.filter(
            lambda x: x.rule == self.target_rule
            and x.members.where(is_slot=False) == suggested_members
        ).is_empty()

    def _calculate_confidence(self):
        if self.target_rule.right_concept is None:
            branch_concept = self.target_rule.left_concept
            self.target_branch = "left"
        else:
            branch_names = {
                self.target_rule.left_concept: "left",
                self.target_rule.right_concept: "right",
            }
            branch_concept = self.bubble_chamber.random_machine.select(
                [self.target_rule.left_concept, self.target_rule.right_concept],
                key=lambda x: self.target_rule.compatibility_with(
                    collection=self.bubble_chamber.new_structure_collection(
                        self.target_node
                    ),
                    branch=branch_names[x],
                ),
            )
            self.target_branch = branch_names[branch_concept]
        classifications = [
            branch_concept.classifier.classify(
                collection=self.bubble_chamber.new_structure_collection(
                    self.target_node
                ),
                concept=branch_concept,
            )
        ]
        self.confidence = fuzzy.AND(*classifications)

    def _fizzle(self):
        pass
