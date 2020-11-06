from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures.space import Space

from .working_space import WorkingSpace


class ConceptualSpace(Space):
    def __init__(
        self,
        contents: StructureCollection,
        links_in: StructureCollection,
        links_out: StructureCollection,
    ):
        quality = None
        Space.__init__(self, contents, quality, links_in=links_in, links_out=links_out)
        self._instance = None

    @property
    def instance(self) -> WorkingSpace:
        if self._instance is None:
            self._instance = WorkingSpace(
                StructureCollection(),
                FloatBetweenOneAndZero(0),
                links_in=StructureCollection(),
                links_out=StructureCollection(),
            )
        return self._instance
