from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Space

from .working_space import WorkingSpace


class ConceptualSpace(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        contents: StructureCollection,
        parent_concept: Concept,
        parent_spaces: StructureCollection = None,
        child_spaces: StructureCollection = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        quality = None
        Space.__init__(
            self,
            structure_id,
            parent_id,
            name,
            contents,
            quality,
            parent_concept,
            parent_spaces=parent_spaces,
            child_spaces=child_spaces,
            links_in=links_in,
            links_out=links_out,
        )
        self._instance = None

    @property
    def instance(self) -> WorkingSpace:
        if self._instance is None:
            self._instance = WorkingSpace(
                self.structure_id + "_working_space",
                self.structure_id,
                self.name + " working",
                StructureCollection(),
                FloatBetweenOneAndZero(0),
                self.parent_concept,
                links_in=StructureCollection(),
                links_out=StructureCollection(),
            )
        return self._instance

    def update_activation(self):
        self._activation = max(item.activation for item in self.contents)
