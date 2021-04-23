from __future__ import annotations
import random
from typing import List, Optional, Set, Union

from .errors import MissingStructureError
from .location import Location


class StructureCollection:
    def __init__(self, structures: Optional[Set] = None):
        self.structures = set() if structures is None else structures
        self.structures_by_name = None

    def __len__(self):
        return len(self.structures)

    def __eq__(self, other: StructureCollection) -> bool:
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

    def copy(self) -> StructureCollection:
        return StructureCollection({structure for structure in self.structures})

    def is_empty(self) -> bool:
        return len(self) == 0

    def at(self, location: Location) -> StructureCollection:
        return StructureCollection(
            {
                structure
                for coordinates in location.coordinates
                for structure in self.structures
                if coordinates in structure.location.coordinates
            }
        )

    def next_to(self, location: Location) -> StructureCollection:
        left_most_coordinate = location.coordinates[0][0]
        right_most_coordinate = location.coordinates[-1][0]
        return StructureCollection(
            {
                structure
                for structure in location.space.contents
                if structure.location_in_space(location.space).coordinates != []
                and (
                    structure.location.coordinates[-1][0] == left_most_coordinate - 1
                    or structure.location.coordinates[0][0] == right_most_coordinate + 1
                )
            }
        )

    def near(self, location: Location) -> StructureCollection:
        return StructureCollection(
            {
                structure
                for structure in self.structures
                if structure.location.is_near(location)
            }
        )

    def where(self, **kwargs) -> StructureCollection:
        old_collection = self
        for key, value in kwargs.items():
            new_collection = StructureCollection()
            for structure in old_collection:
                if hasattr(structure, key) and getattr(structure, key) == value:
                    new_collection.add(structure)
            old_collection = new_collection
        return new_collection

    def where_not(self, **kwargs) -> StructureCollection:
        old_collection = self
        for key, value in kwargs.items():
            new_collection = StructureCollection()
            for structure in old_collection:
                if hasattr(structure, key) and getattr(structure, key) != value:
                    new_collection.add(structure)
            old_collection = new_collection
        return new_collection

    def add(self, structure):
        self.structures.add(structure)
        if self.structures_by_name is not None and hasattr(structure, "name"):
            self.structures_by_name[structure.name] = structure

    def remove(self, structure):
        self.structures.discard(structure)
        if self.structures_by_name is not None and hasattr(structure, "name"):
            try:
                self.structures_by_name.pop(structure.name)
            except KeyError:
                pass

    def pop(self):
        structure = self.get_random()
        self.remove(structure)
        return structure

    @staticmethod
    def union(*collections: List[StructureCollection]) -> StructureCollection:
        if len(collections) == 0:
            return StructureCollection()
        return StructureCollection(
            set.union(*[collection.structures for collection in collections])
        )

    @staticmethod
    def intersection(*collections: List[StructureCollection]) -> StructureCollection:
        return StructureCollection(
            set.intersection(*[collection.structures for collection in collections])
        )

    @staticmethod
    def difference(
        a: StructureCollection, b: StructureCollection
    ) -> StructureCollection:
        return StructureCollection(set.difference(a.structures, b.structures))

    def of_type(self, t: type) -> StructureCollection:
        return StructureCollection(
            {element for element in self.structures if isinstance(element, t)}
        )

    def not_of_type(self, t: type) -> StructureCollection:
        return StructureCollection(
            {element for element in self.structures if not isinstance(element, t)}
        )

    def proportion_with_label(self, concept):
        return self.number_with_label(concept) / len(self)

    def number_with_label(self, concept):
        return sum(1 for structure in self.structures if structure.has_label(concept))

    def get_random(self, exclude: list = None):
        """Returns a random structure"""
        if len(self.structures) < 1:
            raise MissingStructureError
        if exclude is not None:
            return StructureCollection.difference(
                self, StructureCollection(set(exclude))
            ).get_random()
        return random.sample(self.structures, 1)[0]

    def get_exigent(self, exclude: list = None):
        """Returns a structure probabilistically according to exigency."""
        return self._get_structure_according_to("exigency", exclude)

    def get_active(self, exclude: list = None):
        """Returns a structure probabilistically according to activation."""
        return self._get_structure_according_to("activation", exclude)

    def get_most_active(self):
        return self._get_structure_with_highest("activation")

    def get_unhappy(self, exclude: list = None):
        """Returns a structure probabilistically according to unhappiness."""
        return self._get_structure_according_to("unhappiness", exclude)

    def __repr__(self) -> str:
        return "{" + ", ".join(repr(structure) for structure in self.structures) + "}"

    def _get_structure_according_to(self, attribute: str, exclude: list = None):
        """Returns a structure probabilistically according to attribute."""
        if len(self.structures) < 1:
            raise MissingStructureError
        if exclude is not None:
            return StructureCollection.difference(
                self, StructureCollection(set(exclude))
            )._get_structure_according_to(attribute)
        if len(self.structures) == 1:
            return list(self.structures)[0]
        structures = random.sample(self.structures, len(self.structures) // 2)
        structure_choice = structures[0]
        for structure in structures[1:]:
            if getattr(structure, attribute) > getattr(structure_choice, attribute):
                structure_choice = structure
        return structure_choice

    def _get_structure_with_highest(self, attribute: str):
        structure_choice = self.get_random()
        for structure in self.structures:
            if getattr(structure, attribute) > getattr(structure_choice, attribute):
                structure_choice = structure
        return structure_choice

    def _arrange_structures_by_name(self):
        self.structures_by_name = {}
        for item in self.structures:
            if hasattr(item, "name"):
                self.structures_by_name[item.name] = item
