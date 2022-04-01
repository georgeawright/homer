from __future__ import annotations
from typing import List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection


class LinkOrNode(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        locations: List[Location],
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        parent_space: "Space" = None,
    ):
        Structure.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            locations=locations,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
        )
        self._parent_space = parent_space
        self.is_link_or_node = True
        self.is_link = True
        self.is_node = True

    def __dict__(self) -> dict:
        return {}

    def copy_with_contents(
        self,
        copies: dict,
        bubble_chamber: "BubbleChamber",
        parent_id: str,
        new_location: Location,
    ):
        new_locations = [
            location
            for location in self.locations
            if location.space.is_conceptual_space
        ] + [new_location]
        link_or_node_copy = LinkOrNode(
            structure_id=ID.new(LinkOrNode),
            parent_id=parent_id,
            locations=new_locations,
            parent_space=new_location.space,
            quality=self.quality,
            links_in=bubble_chamber.new_structure_collection(),
            links_out=bubble_chamber.new_structure_collection(),
            parent_spaces=bubble_chamber.new_structure_collection(
                *[location.space for location in new_locations]
            ),
        )
        bubble_chamber.loggers["structure"].log(link_or_node_copy)
        return (link_or_node_copy, copies)

    def __repr__(self) -> str:
        if self.parent_space is None:
            return f"<{self.structure_id}>"
        return f"<{self.structure_id} in {self.parent_space.structure_id} {self.locations}>"
