from typing import List

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunk import Chunk
from homer.structures.link import Link


class Text(Chunk):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        location: Location,
        members: StructureCollection,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        value = " ".join(member.value for member in members)
        location = None
        Chunk.__init__(
            structure_id,
            parent_id,
            value,
            location,
            members,
            quality,
            links_in=links_in,
            links_out=links_out,
        )
