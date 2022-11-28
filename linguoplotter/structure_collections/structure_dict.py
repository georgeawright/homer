from __future__ import annotations
from typing import Dict

from linguoplotter.structure_collection import StructureCollection


class StructureDict(StructureCollection):
    def __init__(
        self,
        bubble_chamber: "BubbleChamber",
        structures: Dict["str", "Structure"],
        name: str = None,
    ):
        StructureCollection.__init__(self, bubble_chamber, structures, name=name)

    def __getitem__(self, name: str):
        try:
            return self.structures[name]
        except KeyError:
            return None

    def __setitem__(self, name: str, structure: "Structure"):
        self.structures[name] = structure
        if self.name != None:
            self.bubble_chamber.loggers["activity"].log(
                f"{self.name} {name} set to {structure}"
            )

    def items(self):
        return self.structures.items()

    def keys(self):
        return self.structures.keys()

    def values(self):
        return self.structures.values()

    def __repr__(self) -> str:
        return (
            "{"
            + ", ".join(
                f"{key}: {structure}" for key, structure in self.structures.items()
            )
            + "}"
        )
