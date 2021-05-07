from typing import Any, List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection

from .space import Space


class Node(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        value: Any,
        locations: List[Location],
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
        stable_activation: FloatBetweenOneAndZero = None,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            locations,
            quality,
            links_in=links_in,
            links_out=links_out,
            stable_activation=stable_activation,
        )
        self._value = value
        self._parent_space = parent_space
        self.is_node = True

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any):
        self._value = value

    @property
    def parent_space(self) -> Space:
        return self._parent_space

    @parent_space.setter
    def parent_space(self, space: Space):
        self._parent_space = space

    @property
    def is_slot(self):
        return self.value is None

    @property
    def unchunkedness(self) -> FloatBetweenOneAndZero:
        return 0

    def nearby(self, space: Space = None) -> StructureCollection:
        if space is not None:
            return StructureCollection.difference(
                space.contents.of_type(type(self)).near(self.location_in_space(space)),
                StructureCollection({self}),
            )
        nearby_nodes = StructureCollection.union(
            *[
                location.space.contents.of_type(type(self)).near(location)
                for location in self.locations
            ]
        )
        nearby_nodes.remove(self)
        return nearby_nodes

    def __repr__(self) -> str:
        return f"<{self.structure_id} {self.value} in {self.parent_space.structure_id}>"
