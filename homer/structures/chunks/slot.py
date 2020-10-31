from typing import Any

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunk import Chunk


class Slot(Chunk):
    """A piece of a frame which acts as a replaceable prototype"""

    def __init__(
        self,
        value: Any = None,
        location: Location = None,
        members: StructureCollection = None,
        neighbours: StructureCollection = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Chunk.__init__(self, value, location, members, neighbours, links_in, links_out)
