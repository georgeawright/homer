from typing import List

from homer.structures.chunk import Chunk
from homer.structures.link import Link


class Lexeme(Structure):
    def __init__(
        self,
        headword: str,
        links_in: List[Link] = None,
        links_out: List[Link] = None,
    ):
        location = None
        members = []
        neighbours = []
        links_in = [] if links_in is None else links_in
        links_out = [] if links_out is None else links_out
        hunk.__init(self, headword, location, members, neighbours, links_in, links_out)
        self.headword = headword
