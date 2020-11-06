from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structure_collection import StructureCollection


class Space(Structure):
    def __init__(
        self,
        contents: list,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
    ):
        location = None
        Structure.__init__(
            self, location, quality, links_in=links_in, links_out=links_out
        )
        self.contents = contents
