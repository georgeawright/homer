from typing import List

from homer.structures.chunk import Chunk
from homer.structures.link import Link

from .concept import Concept
from .slot import Slot


class Frame(Chunk):
    def __init__(
        self,
        members: List[Union[Concept, Slot]],
        links_in: List[Link] = None,
        links_out: List[Link] = None,
    ):
        value = None
        location = None
        neighbours = []
        links_in = [] if links_in is None else links_in
        links_out = [] if links_out is None else links_out
        Chunk.__init__(value, members, neighbours, links_in, links_out)
