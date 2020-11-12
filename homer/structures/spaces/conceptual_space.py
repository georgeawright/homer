from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Space

from .working_space import WorkingSpace


class ConceptualSpace(Space):
    def __init__(
        self,
        name: str,
        contents: StructureCollection,
        parent_concept: Concept,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        quality = None
        Space.__init__(
            self,
            name,
            contents,
            quality,
            parent_concept,
            links_in=links_in,
            links_out=links_out,
        )
        self._instance = None

    @property
    def instance(self) -> WorkingSpace:
        if self._instance is None:
            self._instance = WorkingSpace(
                self.name + " working",
                StructureCollection(),
                FloatBetweenOneAndZero(0),
                self.parent_concept,
                links_in=StructureCollection(),
                links_out=StructureCollection(),
            )
        return self._instance
