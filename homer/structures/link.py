from homer.structure import Structure
from homer.structure_collection import StructureCollection


class Link(Structure):
    def __init__(
        self,
        start: Structure,
        end: Structure,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Structure.__init__(self, start.location, links_in, links_out)
        self.start = start
        self.end = end

    def is_between(self, a: Structure, b: Structure):
        return self.start == a and self.end == b or self.end == a and self.start == a
