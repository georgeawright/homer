from homer.structure_collection import StructureCollection
from homer.structures.space import Space


class WorkingSpace(Space):
    def __init__(
        self,
        contents: StructureCollection,
        links_in: StructureCollection,
        links_out: StructureCollection,
    ):
        Space.__init__(self, contents, links_in, links_out)
