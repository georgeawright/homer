from typing import Callable

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
        is_sub_space: bool = False,
        parent_spaces: StructureCollection = None,
        child_spaces: StructureCollection = None,
        coordinates_from_super_space_location: Callable = None,
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
            is_sub_space=is_sub_space,
            parent_spaces=parent_spaces,
            child_spaces=child_spaces,
            coordinates_from_super_space_location=coordinates_from_super_space_location,
            links_in=links_in,
            links_out=links_out,
        )
        self._instance = None

    @property
    def instance(self) -> WorkingSpace:
        if self._instance is None:
            self._instance = WorkingSpace(
                self.structure_id + "_working_space",
                "",
                self.name + " working",
                StructureCollection(),
                FloatBetweenOneAndZero(0),
                self.parent_concept,
                coordinates_from_super_space_location=self.coordinates_from_super_space_location,
                is_sub_space=self.is_sub_space,
                links_in=StructureCollection(),
                links_out=StructureCollection(),
            )
            for sub_space in self.sub_spaces:
                self._instance.sub_spaces.add(sub_space.instance)
        return self._instance

    def update_activation(self):
        self._activation = max(item.activation for item in self.contents)
