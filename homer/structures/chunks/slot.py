from typing import Any, List

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
        locations: List[Location] = None,
        members: StructureCollection = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        containing_chunks: StructureCollection = None,
    ):
        locations = locations if locations is not None else []
        Chunk.__init__(
            self,
            structure_id,
            parent_id,
            value,
            locations,
            members,
            1,
            links_in=links_in,
            links_out=links_out,
            containing_chunks=containing_chunks,
        )
