from __future__ import annotations
from typing import Any, List

from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection

from .link import Link


class Chunk(Structure):
    def __init__(
        self,
        value: Any,
        location: Location,
        members: StructureCollection,
        neighbours: StructureCollection,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Structure.__init__(self, location, links_in, links_out)
        self.value = value
        self.members = members
        self.neighbours = neighbours
        self.links_in = links_in
        self.links_out = links_out

    @property
    def size(self):
        return 1 if self.members == [] else sum(member.size for member in self.members)

    def nearby(self):
        return StructureCollection.intersection(
            space.elements_close_to(self.location) for space in self.spaces
        )

    def add_member(self, new_member: Chunk):
        # alter neightbours
        pass
