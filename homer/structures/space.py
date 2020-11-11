from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structure_collection import StructureCollection


class Space(Structure):
    def __init__(
        self,
        contents: list,
        quality: FloatBetweenOneAndZero,
        parent_concept: "Concept",
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        location = None
        Structure.__init__(
            self, location, quality, links_in=links_in, links_out=links_out
        )
        self.contents = contents
        self.parent_concept = parent_concept

    def distance_between(self, a: Structure, b: Structure):
        return self.parent_concept.distance_between(a, b)

    def proximity_between(self, a: Structure, b: Structure):
        return self.parent_concept.proximity_between(a, b)
