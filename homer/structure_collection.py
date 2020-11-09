from __future__ import annotations
import random
from typing import List, Optional, Set, Union

from .errors import MissingStructureError
from .location import Location


class StructureCollection:
    def __init__(self, structures: Optional[Set] = None):
        self.structures = set() if structures is None else structures
        self.structures_by_location = None

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

    def copy(self) -> StructureCollection:
        return StructureCollection({structure for structure in self.structures})

    def is_empty(self) -> bool:
        return len(self) == 0

    def at(self, location: Location) -> StructureCollection:
        if self.structures_by_location is None:
            self._arrange_structures_by_location()
        return StructureCollection(
            self.structures_by_location[location.i][location.j][location.k]
        )

    def add(self, structure):
        self.structures.add(structure)
        if self.structures_by_location is not None:
            self._add_at_location(structure, structure.location)
            if hasattr(structure, "members"):
                for member in structure.members:
                    self._add_at_location(structure, member.location)

    def remove(self, structure):
        self.structures.discard(structure)
        if self.structures_by_location is None:
            return
        for i, layer in enumerate(self.structures_by_location):
            for j, row in enumerate(layer):
                for k, cell in enumerate(row):
                    if structure in cell:
                        self.structures_by_location[i][j][k].discard(structure)

    @staticmethod
    def union(*collections: List[StructureCollection]) -> StructureCollection:
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

    def proportion_with_label(self, concept: Concept):
        return self.number_with_label(concept) / len(self)

    def number_with_label(self, concept: Concept):
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

    def _add_at_location(self, structure, coordinates: List[Union[float, int]]):
        loc = Location.from_workspace_coordinates(coordinates)
        self.structures_by_location[loc.i][loc.j][loc.k].add(structure)

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

    def _arrange_structures_by_location(self):
        self.structures_by_location = [
            [[set() for _ in range(Location.WIDTH)] for _ in range(Location.HEIGHT)]
            for _ in range(Location.DEPTH)
        ]
        for structure in self.structures:
            loc = Location.from_workspace_coordinates(structure.location)
            self.structures_by_location[loc.i][loc.j][loc.k].add(structure)
