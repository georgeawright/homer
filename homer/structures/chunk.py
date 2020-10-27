from typing import Any

from homer.location import Location
from homer.structure import Structure


class Chunk(Structure):
    def __init__(
        self,
        value: Any,
        location: Location,
        members: List[Structure],
        neighbours: List[Structure],
        links_in: List[Link],
        links_out: List[Link],
    ):
        Structure.__init__(self, Location, links_in, links_out)
        self.members = members
        self.neighbours = neighbours
        self.links_in = links_in
        self.links_out = links_out

    @property
    def size(self):
        return 1 if self.members == [] else sum(member.size for member in self.members)

    def nearby(self):
        return self.neighbours

    def add_member(self, new_member: Chunk):
        pass
