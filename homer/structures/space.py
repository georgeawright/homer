from homer.structure import Structure
from homer.structure_collection import StructureCollection


class Space(Structure):
    def __init__(
        self,
        contents: list,
        links_in: StructureCollection,
        links_out: StructureCollection,
    ):
        Structure.__init__(self, None, links_in, links_out)
        self.contents = contents
