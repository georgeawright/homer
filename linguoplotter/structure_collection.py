from __future__ import annotations
from typing import List

from .errors import MissingStructureError
from .location import Location


class StructureCollection:
    def __init__(self, bubble_chamber: "BubbleChamber", structures: List["Structure"]):
        self.bubble_chamber = bubble_chamber
        self.structures = {structure: True for structure in structures}
        self.structures_by_name = None

    @staticmethod
    def union(*collections: List[StructureCollection]) -> StructureCollection:
        return StructureCollection(
            collections[0].bubble_chamber,
            [structure for collection in collections for structure in collection],
        )

    @staticmethod
    def intersection(*collections: List[StructureCollection]) -> StructureCollection:
        structures = [
            structure for collection in collections for structure in collection
        ]
        for collection in collections:
            structures = [
                structure for structure in structures if structure in collection
            ]
        return StructureCollection(collections[0].bubble_chamber, structures)

    @staticmethod
    def difference(
        a: StructureCollection, b: StructureCollection
    ) -> StructureCollection:
        return StructureCollection(
            a.bubble_chamber, [structure for structure in a if structure not in b]
        )

    @property
    def pairs(self) -> StructureCollection:
        return StructureCollection(
            self.bubble_chamber,
            [(a, b) for a in self.structures for b in self.structures],
        )

    def __len__(self):
        return len(self.structures)

    def __eq__(self, other: StructureCollection) -> bool:
        if other is None:
            return False
        if len(self) != len(other):
            return False
        for structure in self:
            if structure not in other:
                return False
        return True

    def __ne__(self, other: StructureCollection) -> bool:
        return not self == other

    def __iter__(self):
        return (structure for structure in self.structures)

    def __getitem__(self, name: str):
        if self.structures_by_name is None:
            self._arrange_structures_by_name()
        return self.structures_by_name[name]

    def __repr__(self) -> str:
        return "{" + ", ".join(repr(structure) for structure in self.structures) + "}"

    def copy(self) -> StructureCollection:
        return StructureCollection(
            self.bubble_chamber, [structure for structure in self.structures]
        )

    def is_empty(self) -> bool:
        return len(self) == 0

    def filter(self, *filters: List[callable]) -> StructureCollection:
        old_collection = self
        for f in filters:
            new_collection = StructureCollection(
                self.bubble_chamber,
                [structure for structure in old_collection if f(structure)],
            )
            old_collection = new_collection
        return new_collection

    def excluding(self, *structures) -> StructureCollection:
        return self.filter(lambda x: x not in structures)

    def at(self, location: Location) -> StructureCollection:
        def _at(structure):
            for coordinates in location.coordinates:
                if coordinates in structure.location.coordinates:
                    return True
            return False

        return self.filter(_at)

    def next_to(self, location: Location) -> StructureCollection:
        left_most_coordinate = location.coordinates[0][0]
        right_most_coordinate = location.coordinates[-1][0]
        return self.filter(
            lambda x: x.location_in_space(location.space).coordinates != []
            and (
                x.location.coordinates[-1][0] == left_most_coordinate - 1
                or x.location.coordinates[0][0] == right_most_coordinate + 1
            )
        )

    def near(self, location: Location) -> StructureCollection:
        return self.filter(
            lambda x: x.location_in_space(location.space).is_near(location)
            if location.space.parent_concept.distance_function is not None
            else True
        )

    def where(self, **kwargs) -> StructureCollection:
        old_collection = self
        for key, value in kwargs.items():
            new_collection = StructureCollection(self.bubble_chamber, [])
            for structure in old_collection:
                if hasattr(structure, key) and getattr(structure, key) == value:
                    new_collection.add(structure)
            old_collection = new_collection
        return new_collection

    def where_not(self, **kwargs) -> StructureCollection:
        old_collection = self
        for key, value in kwargs.items():
            new_collection = StructureCollection(self.bubble_chamber, [])
            for structure in old_collection:
                if hasattr(structure, key) and getattr(structure, key) != value:
                    new_collection.add(structure)
            old_collection = new_collection
        return new_collection

    def add(self, structure):
        self.structures[structure] = True
        if self.structures_by_name is not None and hasattr(structure, "name"):
            self.structures_by_name[structure.name] = structure

    def remove(self, structure):
        self.structures.pop(structure, None)
        if self.structures_by_name is not None and hasattr(structure, "name"):
            self.structures_by_name.pop(structure.name, None)

    def pop(self):
        structure = self.get()
        self.remove(structure)
        return structure

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

    def sample(self, size: int, key: callable = lambda x: 0, exclude: list = None):
        if len(self) < size:
            raise MissingStructureError
        exclude = [] if exclude is None else exclude
        collection = StructureCollection(self.bubble_chamber, [])
        for _ in range(size):
            item = self.get(key, exclude)
            exclude.append(item)
            collection.add(item)
        return collection

    def _arrange_structures_by_name(self):
        self.structures_by_name = {}
        for item in self.structures:
            if hasattr(item, "name"):
                self.structures_by_name[item.name] = item
