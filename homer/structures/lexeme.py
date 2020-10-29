from typing import List

from homer.structure import Structure
from homer.structure_collection import StructureCollection


class Lexeme(Structure):
    def __init__(
        self,
        headword: str,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        location = None
        Structure.__init(self, location, links_in, links_out)
        self.headword = headword
