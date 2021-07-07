from typing import List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Node
from homer.tools import arrange_text_fragments

from .concept import Concept


class Rule(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        location: Location,
        root: Concept,
        left_branch: Concept,
        right_branch: Concept,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        stable_activation: FloatBetweenOneAndZero = None,
    ):
        quality = None
        Node.__init__(
            self,
            structure_id,
            parent_id,
            locations=[location],
            parent_space=location.space,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            stable_activation=stable_activation,
        )
        self.name = name
        self._value = name
        self.root = root
        self.left_branch = left_branch
        self.right_branch = right_branch

    @property
    def rule_constituents(self) -> StructureCollection:
        return StructureCollection({self.root, self.left_branch, self.right_branch})

    def is_compatible_with(self, *fragments: List[Structure]) -> bool:
        if len(fragments) == 1:
            fragment = fragments[0]
            return (
                fragment.parent_concept == self.root
                or fragment.parent_concept == self.left_branch
                or fragment.parent_concept == self.right_branch
                or fragment.has_label(self.left_branch)
                or fragment.has_label(self.right_branch)
            )
        try:
            arranged_fragments = arrange_text_fragments(fragments)
        except Exception:
            return False
        return (
            (
                arranged_fragments["root"] is None
                or arranged_fragments["root"].parent_concept == self.root
            )
            and (
                arranged_fragments["left"] is None
                or arranged_fragments["left"].parent_concept == self.left_branch
                or arranged_fragments["left"].has_label(self.left_branch)
            )
            and (
                arranged_fragments["right"] is None
                or arranged_fragments["right"].parent_concept == self.right_branch
                or arranged_fragments["right"].has_label(self.right_branch)
            )
        )
