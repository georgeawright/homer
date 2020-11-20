import statistics

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Space


class WorkingSpace(Space):
    def __init__(
        self,
        name: str,
        contents: StructureCollection,
        quality: FloatBetweenOneAndZero,
        parent_concept: Concept,
        parent_spaces: StructureCollection = None,
        child_spaces: StructureCollection = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Space.__init__(
            self,
            name,
            contents,
            quality,
            parent_concept,
            parent_spaces=parent_spaces,
            child_spaces=child_spaces,
            links_in=links_in,
            links_out=links_out,
        )

    def update_activation(self):
        self._activation = statistics.median(
            [item.activation for item in self.contents]
        )
