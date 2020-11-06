from homer.structure_collection import StructureCollection
from homer.structures.space import Space


class Frame(Space):
    def __init__(
        self,
        contents: StructureCollection,
        links_in: StructureCollection,
        links_out: StructureCollection,
    ):
        quality = None
        Space.__init__(self, contents, quality, links_in=links_in, links_out=links_out)
