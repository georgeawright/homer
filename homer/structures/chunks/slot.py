from typing import Any

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunk import Chunk


class Slot(Chunk):
    """A piece of a frame which acts as a replaceable prototype"""

    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        value: Any = None,
        location: Location = None,
        members: StructureCollection = None,
        parent_spaces: StructureCollection = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Chunk.__init__(
            self,
            structure_id,
            parent_id,
            value,
            location,
            members,
            None,
            parent_spaces,
            links_in=links_in,
            links_out=links_out,
        )
