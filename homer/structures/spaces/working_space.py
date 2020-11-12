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
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Space.__init__(
            self,
            name,
            contents,
            quality,
            parent_concept,
            links_in=links_in,
            links_out=links_out,
        )
