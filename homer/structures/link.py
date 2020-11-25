from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structure_collection import StructureCollection


class Link(Structure):
    def __init__(
        self,
        start: Structure,
        end: Structure,
        parent_concept: "Concept",
        parent_space: "Space",
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Structure.__init__(
            self, start.location, quality, links_in=links_in, links_out=links_out
        )
        self.start = start
        self.end = end
        self.parent_concept = parent_concept
        self.parent_space = parent_space
        self.parent_spaces = StructureCollection({parent_space})

    def is_between(self, a: Structure, b: Structure):
        return self.start == a and self.end == b or self.end == a and self.start == a

    def spread_activation(self):
        if not self.is_fully_active():
            return
        self.parent_concept.boost_activation()
