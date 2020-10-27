from typing import List

from homer.structures.chunks.slot import Slot
from homer.structures.chunks.word import Word
from homer.structures.spaces.frame import Frame
from homer.structures.link import Link


class Template(Frame):
    def __init__(
        self,
        members: List[Union[Slot, Word]],
        links_in: List[Link] = None,
        links_out: List[Link] = None,
    ):
        value = " ".join(member.value for member in members)
        location = None
        neighbours = []
        links_in = [] if links_in is None else links_in
        links_out = [] if links_out is None else links_out
        Frame.__init__(value, members, neighbours, links_in, links_out)
