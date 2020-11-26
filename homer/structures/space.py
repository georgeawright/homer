from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structure_collection import StructureCollection


class Space(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        contents: list,
        quality: FloatBetweenOneAndZero,
        parent_concept: "Concept",
        parent_spaces: StructureCollection = None,
        child_spaces: StructureCollection = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        location = None
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            location,
            quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.name = name
        self.value = name
        self.contents = contents
        self.parent_concept = parent_concept
        self.parent_spaces = (
            parent_spaces if parent_spaces is not None else StructureCollection()
        )
        self.child_spaces = (
            child_spaces if child_spaces is not None else StructureCollection()
        )

    def distance_between(self, a: Structure, b: Structure):
        return self.parent_concept.distance_between(a, b)

    def proximity_between(self, a: Structure, b: Structure):
        return self.parent_concept.proximity_between(a, b)
