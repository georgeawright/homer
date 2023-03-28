from __future__ import annotations
from typing import List

from linguoplotter.structure_collection import StructureCollection


class StructureList(StructureCollection):
    def __init__(
        self,
        bubble_chamber: "BubbleChamber",
        structures: List["Structure"],
        name: str = None,
    ):
        structures = {structure: True for structure in structures}
        StructureCollection.__init__(self, bubble_chamber, structures, name=name)

    def __dict__(self) -> dict:
        return {
            key: self.structures[key].__dict__()
            if isinstance(self.structures[key], StructureCollection)
            else self.structures[key].structure_id
            for key in range(len(self.structures))
            if self.structures[key] is not None
        }

    def __getitem__(self, index: int):
        return self.structures[index]

    def __setitem__(self, index: int, structure: "Structure"):
        self.structures[index] = structure
        if self.name != None:
            self.bubble_chamber.loggers["activity"].log(
                f"Index {index} of {self.name} set to {structure}"
            )

    def values(self):
        return self.structures

    def append(self, structure: "Structure"):
        self.structures.append(structure)

    def __repr__(self) -> str:
        return "[" + ", ".join(f"{structure}" for structure in self.structures) + "]"
