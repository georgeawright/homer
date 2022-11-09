from __future__ import annotations
from typing import List

from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection import StructureCollection


class StructureSet(StructureCollection):
    def __init__(
        self,
        bubble_chamber: "BubbleChamber",
        structures: List["Structure"],
        name: str = None,
    ):
        structures = {structure: True for structure in structures}
        StructureCollection.__init__(self, bubble_chamber, structures, name=name)
        self.structures_by_name = None

    @staticmethod
    def union(*structure_sets: List[StructureSet]) -> StructureSet:
        return StructureSet(
            structure_sets[0].bubble_chamber,
            [
                structure
                for structure_set in structure_sets
                for structure in structure_set
            ],
        )

    @staticmethod
    def intersection(*structure_sets: List[StructureSet]) -> StructureSet:
        structures = [
            structure for structure_set in structure_sets for structure in structure_set
        ]
        for structure_set in structure_sets:
            structures = [
                structure for structure in structures if structure in structure_set
            ]
        return StructureSet(structure_sets[0].bubble_chamber, structures)

    @staticmethod
    def difference(a: StructureSet, b: StructureSet) -> StructureSet:
        return StructureSet(
            a.bubble_chamber, [structure for structure in a if structure not in b]
        )

    def __getitem__(self, name: str):
        if self.structures_by_name is None:
            self._arrange_structures_by_name()
        return self.structures_by_name[name]

    def __repr__(self) -> str:
        return "{" + ", ".join(repr(structure) for structure in self.structures) + "}"

    def values(self):
        return self.structures.keys()

    def sample(
        self, size: int, key: callable = lambda x: 0, exclude: list = None
    ) -> StructureSet:
        exclude = [] if exclude is None else exclude
        sample_set = StructureSet(self.bubble_chamber, [])
        for _ in range(size):
            item = self.get(key, exclude)
            exclude.append(item)
            sample_set.add(item)
        return sample_set

    def add(self, structure):
        self.structures[structure] = True
        if self.structures_by_name is not None and hasattr(structure, "name"):
            self.structures_by_name[structure.name] = structure
        if self.name != None:
            self.bubble_chamber.loggers["activity"].log(
                f"{structure} added to {self.name}"
            )

    def remove(self, structure):
        self.structures.pop(structure, None)
        if self.structures_by_name is not None and hasattr(structure, "name"):
            self.structures_by_name.pop(structure.name, None)
        if self.name != None:
            self.bubble_chamber.loggers["activity"].log(
                f"{structure} removed from {self.name}"
            )

    def pop(self):
        structure = self.get()
        self.remove(structure)
        return structure

    def _arrange_structures_by_name(self):
        self.structures_by_name = {}
        for item in self.structures:
            if hasattr(item, "name"):
                self.structures_by_name[item.name] = item
