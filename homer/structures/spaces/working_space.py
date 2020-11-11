from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures.space import Space


class WorkingSpace(Space):
    def __init__(
        self,
        contents: StructureCollection,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Space.__init__(self, contents, quality, links_in=links_in, links_out=links_out)
