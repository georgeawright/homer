from __future__ import annotations
from typing import List

from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Link, View
from homer.structures.nodes import Concept
from homer.structures.spaces import ConceptualSpace


class Correspondence(Link):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        start: Structure,
        arguments: StructureCollection,
        locations: List[Location],
        parent_concept: Concept,
        conceptual_space: ConceptualSpace,
        parent_view: View,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        is_privileged: bool = False,
    ):
        Link.__init__(
            self,
            structure_id,
            parent_id,
            start,
            arguments,
            locations,
            parent_concept,
            quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
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

    @property
    def node_pairs(self) -> list:
        if self.start.is_node:
            return [(self.start, self.end)]
        if self.start.is_label:
            return [(self.start.start, self.end.start)]
        return [(self.start.start, self.end.start), (self.start.end, self.end.end)]

    def copy(self, **kwargs: dict) -> Correspondence:
        """Requires keyword arguments 'start', 'end', and 'parent_id' OR 'new arg', 'old_arg', and 'parent_id'."""
        bubble_chamber = kwargs["bubble_chamber"]
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
            bubble_chamber.new_structure_collection(start, end),
            [
                start.location_in_space(start.parent_space),
                end.location_in_space(end.parent_space),
            ],
            self.parent_concept,
            self.conceptual_space,
            self.parent_view,
            self.quality,
            bubble_chamber.new_structure_collection(),
            bubble_chamber.new_structure_collection(),
            bubble_chamber.new_structure_collection(),
            is_privileged=self.is_privileged,
        )
        return new_correspondence

    def nearby(self):
        return StructureCollection.difference(
            StructureCollection.union(
                self.start.correspondences_to_space(self.end.parent_space),
                self.end.correspondences_to_space(self.start.parent_space),
            ),
            StructureCollection.intersection(
                self.start.correspondences_to_space(self.end.parent_space),
                self.end.correspondences_to_space(self.start.parent_space),
            ),
        )

    @property
    def slot_argument(self):
        if self.start.is_slot:
            return self.start
        if self.end.is_slot:
            return self.end
        raise MissingStructureError("Correspondence has no slot argument")

    @property
    def non_slot_argument(self):
        if not self.start.is_slot:
            return self.start
        if not self.end.is_slot:
            return self.end
        raise Exception("Correspondence has no non slot argument")

    def common_arguments_with(self, other: Correspondence) -> StructureCollection:
        return StructureCollection.intersection(self.arguments, other.arguments)

    def __repr__(self) -> str:
        return (
            f"<{self.structure_id} {self.parent_concept.name}("
            + f"{self.start.structure_id}, {self.end.structure_id})>"
        )
