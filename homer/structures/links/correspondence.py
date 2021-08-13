from __future__ import annotations
import operator
from typing import List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Link, Node, Space, View
from homer.structures.nodes import Concept
from homer.structures.spaces import ConceptualSpace
from homer.tools import areinstances, hasinstance

from .label import Label
from .relation import Relation


class Correspondence(Link):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        start: Structure,
        end: Structure,
        locations: List[Location],
        parent_concept: Concept,
        conceptual_space: ConceptualSpace,
        parent_view: View,
        quality: FloatBetweenOneAndZero,
        is_privileged: bool = False,
    ):
        Link.__init__(
            self,
            structure_id,
            parent_id,
            start,
            end,
            locations,
            parent_concept,
            quality,
            links_in=None,
            links_out=None,
        )
        self.conceptual_space = conceptual_space
        self.parent_view = parent_view
        self.is_privileged = is_privileged
        self.is_correspondence = True

    @classmethod
    def get_builder_class(cls):
        from homer.codelets.builders import CorrespondenceBuilder

        return CorrespondenceBuilder

    @classmethod
    def get_evaluator_class(cls):
        from homer.codelets.evaluators import CorrespondenceEvaluator

        return CorrespondenceEvaluator

    @classmethod
    def get_selector_class(cls):
        from homer.codelets.selectors import CorrespondenceSelector

        return CorrespondenceSelector

    def copy(self, **kwargs: dict) -> Correspondence:
        """Requires keyword arguments 'start', 'end', and 'parent_id' OR 'new arg', 'old_arg', and 'parent_id'."""
        if "start" in kwargs:
            start = kwargs["start"]
        else:
            start = (
                kwargs["new_arg"]
                if kwargs["new_arg"] is not None and kwargs["old_arg"] == self.start
                else self.start
            )
        if "end" in kwargs:
            end = kwargs["end"]
        else:
            end = (
                kwargs["new_arg"]
                if kwargs["new_arg"] is not None and kwargs["old_arg"] == self.end
                else self.end
            )
        parent_id = kwargs["parent_id"]
        new_correspondence = Correspondence(
            ID.new(Correspondence),
            parent_id,
            start,
            end,
            [
                start.location_in_space(start.parent_space),
                end.location_in_space(end.parent_space),
            ],
            self.parent_concept,
            self.conceptual_space,
            self.parent_view,
            self.quality,
            is_privileged=self.is_privileged,
        )
        return new_correspondence

    def nearby(self):
        return StructureCollection.difference(
            StructureCollection.union(
                self.start.correspondences,
                self.end.correspondences,
            ),
            StructureCollection({self}),
        )

    @property
    def slot_argument(self):
        if self.start.is_slot:
            return self.start
        if self.end.is_slot:
            return self.end
        raise Exception("Correspondence has no slot argument")

    @property
    def non_slot_argument(self):
        if not self.start.is_slot:
            return self.start
        if not self.end.is_slot:
            return self.end
        raise Exception("Correspondence has no non slot argument")

    def common_arguments_with(self, other: Correspondence) -> StructureCollection:
        return StructureCollection(
            set.intersection({self.start, self.end}, {other.start, other.end})
        )

    def is_compatible_with(self, other: Correspondence) -> bool:
        common_arguments = self.common_arguments_with(other)
        if len(common_arguments) == 2:
            return False
        if hasinstance(self.arguments, Node):
            self_corresponding_nodes = self.arguments
            self_corresponding_links = StructureCollection()
        elif areinstances(self.arguments, Label):
            self_corresponding_nodes = StructureCollection(
                {self.start.start, self.end.start}
            )
            self_corresponding_links = self.arguments
        elif areinstances(self.arguments, Relation):
            self_corresponding_nodes = StructureCollection(
                {self.start.start, self.start.end, self.end.start, self.end.end}
            )
            self_corresponding_links = self.arguments
        if areinstances(other.arguments, Node):
            other_corresponding_nodes = other.arguments
            other_corresponding_links = StructureCollection()
        elif areinstances(other.arguments, Label):
            other_corresponding_nodes = StructureCollection(
                {other.start.start, other.end.start}
            )
            other_corresponding_links = other.arguments
        elif areinstances(other.arguments, Relation):
            other_corresponding_nodes = StructureCollection(
                {other.start.start, other.start.end, other.end.start, other.end.end}
            )
            other_corresponding_links = other.arguments
        if not StructureCollection.intersection(
            self_corresponding_links, other_corresponding_links
        ).is_empty():
            return False
        corresponding_nodes_intersection = StructureCollection.intersection(
            self_corresponding_nodes, other_corresponding_nodes
        )
        if (
            len(self_corresponding_nodes)
            == len(other_corresponding_nodes)
            == len(corresponding_nodes_intersection)
        ):
            return True
        if len(corresponding_nodes_intersection) == 0:
            return True
        if (
            operator.xor(
                areinstances(self.arguments, Relation),
                areinstances(other.arguments, Relation),
            )
            and len(corresponding_nodes_intersection) == 2
        ):
            return True
        return False

    def __repr__(self) -> str:
        return self.structure_id
