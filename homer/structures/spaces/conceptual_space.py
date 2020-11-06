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
        Space.__init__(self, contents, links_in, links_out)
        self._instance = None

    @property
    def instance(self) -> WorkingSpace:
        if self._instance is None:
            self._instance = WorkingSpace(
                StructureCollection(), StructureCollection(), StructureCollection()
            )
        return self._instance
