from typing import List

from homer.structure import Structure


class Lexeme(Structure):
    def __init__(
        self,
        headword: str,
        links_in: List[Structure],
        links_out: List[Structure],
    ):
        Structure.__init(self, None, links_in, links_out)
        self.headword = headword
