from __future__ import annotations
import statistics
from typing import Any, List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.tools import average_vector

from .link import Link
from .space import Space


class Chunk(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        value: Any,
        location: Location,
        members: StructureCollection,
        neighbours: StructureCollection,
        quality: FloatBetweenOneAndZero,
        parent_spaces: StructureCollection,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            location,
            quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.value = value
        self.members = members
        self.neighbours = neighbours
        self.parent_spaces = parent_spaces
        self.locations = [location]

    @property
    def size(self):
        return (
            1 if len(self.members) == 0 else sum(member.size for member in self.members)
        )

    def nearby(self, space: Space = None):
        if space is not None:
            location = [
                location for location in self.locations if location.space == space
            ][0]
            nearby_chunks = space.contents.near(self.location).of_type(type(self))
            nearby_chunks.remove(self)
            return nearby_chunks
        nearby_chunks = StructureCollection.union(
            *[location.space.contents.near(location) for location in self.locations]
        ).of_type(type(self))
        nearby_chunks.remove(self)
        return nearby_chunks

    def add_member(self, new_member: Chunk):
        self.members.add(new_member)
        new_member.neighbours.remove(self)
        for neighbour in new_member.neighbours:
            if neighbour not in self.members:
                self.neighbours.add(neighbour)
        self.neighbours.remove(new_member)
        self.value = self._get_average_value(self.members)
        self.location = self._get_average_location(self.members)

    def _get_average_value(self, chunks: StructureCollection):
        values = []
        for chunk in chunks:
            for _ in range(chunk.size):
                values.append(chunk.value)
        return average_vector(values)

    def _get_average_location(self, chunks: StructureCollection):
        # TODO: needs to be for each space
        locations = []
        for chunk in chunks:
            for _ in range(chunk.size):
                locations.append(chunk.location)
        return Location.average(locations)
