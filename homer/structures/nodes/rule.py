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
        root_concept: Concept,
        left_concept: Concept,
        right_concept: Concept,
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
        self.root_concept = root_concept
        self.left_concept = left_concept
        self.right_concept = right_concept
        self.is_rule = True

    @property
    def rule_constituents(self) -> StructureCollection:
        return StructureCollection(
            {self.root_concept, self.left_concept, self.right_concept}
        )

    @property
    def instance_type(self) -> type:
        return self.left_concept.instance_type

    @property
    def friends(self) -> StructureCollection:
        return StructureCollection.union(
            StructureCollection(
                {
                    link_link.start
                    for link in self.links_in
                    for link_link in link.start.links_in
                }
            ).where(is_rule=True, parent_space=self.parent_space),
            StructureCollection(
                {
                    link_link.end
                    for link in self.links_out
                    for link_link in link.end.links_out
                }
            ).where(is_rule=True, parent_space=self.parent_space),
        )

    def compatibility_with(
        self, root: Node = None, child: Node = None, branch: str = "left"
    ) -> FloatBetweenOneAndZero:
        if root is None:
            if branch == "left":
                return self.left_concept.classifier.classify_chunk(
                    root=root, child=child
                )
            if branch == "right" and self.right_concept is not None:
                return self.right_concept.classifier.classify_chunk(
                    root=root, child=child
                )
            return 0.0
        if branch == "left":
            if self.left_branch_is_free(root):
                return self.left_concept.classifier.classify_chunk(
                    root=root, child=child
                )
            return 0.0
        if self.right_branch_is_free(root):
            return self.right_concept.classifier.classify_chunk(root=root, child=child)
        return 0.0

    def left_branch_is_free(self, root: Node) -> bool:
        return (
            self.left_concept is not None
            and not root.left_branch.where(is_slot=True).is_empty()
        )

    def right_branch_is_free(self, root: Node) -> bool:
        return (
            self.right_concept is not None
            and not root.right_branch.where(is_slot=True).is_empty()
        )

    def is_compatible_with(self, *fragments: List[Structure]) -> bool:
        # TODO: update for chunks
        raise NotImplementedError
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

    def __repr__(self) -> str:
        return f'<{self.structure_id} "{self.name}" in {self.parent_space.name}>'
