from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunk import Chunk


class Word(Chunk):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        value: str,
        location: Location,
        parent_spaces: StructureCollection,
        quality: FloatBetweenOneAndZero,
        members: StructureCollection = None,
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
            quality,
            parent_spaces,
            links_in=links_in,
            links_out=links_out,
        )
