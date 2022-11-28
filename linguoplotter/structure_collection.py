from __future__ import annotations
from typing import Collection, List

from .errors import MissingStructureError
from .location import Location


class StructureCollection:
    def __init__(
        self, bubble_chamber: "BubbleChamber", structures: Collection, name: str = None
    ):
        self.bubble_chamber = bubble_chamber
        self.structures = structures
        self.name = name

    def __len__(self):
        return len(self.structures)

    def __eq__(self, other: StructureCollection) -> bool:
        if not isinstance(other, StructureCollection):
            return False
        if other is None:
            return False
        return (
            self.bubble_chamber == other.bubble_chamber
            and self.structures == other.structures
        )

    def __ne__(self, other: StructureCollection) -> bool:
        return not self == other

    def __iter__(self):
        return (structure for structure in self.structures)

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    @property
    def not_empty(self) -> bool:
        return len(self) > 0

    def copy(self) -> StructureCollection:
        return type(self)(
            self.bubble_chamber, [structure for structure in self.structures]
        )

    def filter(self, *filters: List[callable]) -> StructureCollection:
        old_collection = self
        for f in filters:
            new_collection = type(self)(
                self.bubble_chamber,
                [structure for structure in old_collection if f(structure)],
            )
            old_collection = new_collection
        return new_collection

    def excluding(self, *structures) -> StructureCollection:
        return self.filter(lambda x: x not in structures)

    def near(self, location: Location) -> StructureCollection:
        return self.filter(
            lambda x: x.location_in_space(location.space).is_near(location)
            if location.space.parent_concept.distance_function is not None
            else True
        )

    def where(self, **kwargs) -> StructureCollection:
        return self.filter(
            lambda x: all(
                [
                    hasattr(x, key) and getattr(x, key) == value
                    for key, value in kwargs.items()
                ]
            )
        )

    def where_not(self, **kwargs) -> StructureCollection:
        return self.filter(
            lambda x: all(
                [
                    hasattr(x, key) and getattr(x, key) != value
                    for key, value in kwargs.items()
                ]
            )
        )

    def of_type(self, t: type) -> StructureCollection:
        return StructureCollection(
            self.bubble_chamber,
            [element for element in self.structures if isinstance(element, t)],
        )

    def not_of_type(self, t: type) -> StructureCollection:
        return StructureCollection(
            self.bubble_chamber,
            [element for element in self.structures if not isinstance(element, t)],
        )

    def get(self, key: callable = lambda x: 0, exclude: list = None):
        return self.bubble_chamber.random_machine.select(
            {structure: True for structure in self.structures}, key, exclude
        )
