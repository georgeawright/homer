from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunk import Chunk


class Word(Chunk):
    def __init__(
        self,
        value: str,
        location: Location,
        parent_spaces: StructureCollection,
        members: StructureCollection = None,
        neighbours: StructureCollection = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Chunk.__init__(
            self,
            value,
            location,
            members,
            neighbours,
            parent_spaces,
            links_in,
            links_out,
        )
