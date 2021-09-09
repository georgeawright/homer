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


class ProjectionSuggester(Suggester):
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
        raise NotImplementedError

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        # TODO
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
        # TODO
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
        # TODO ?
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
        raise NotImplementedError

    def _passes_preliminary_checks(self):
        # check for item being projected
        # check item is slot with value filled in
        raise NotImplementedError

    def _calculate_confidence(self):
        self.confidence = (
            self.correspondence_to_non_frame_item.activation if self.is_slot else 1.0
        )

    def _fizzle(self):
        pass
