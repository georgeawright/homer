from typing import List

from homer.structures import Concept
from homer.structures.chunks.slot import Slot
from homer.structures.chunks.word import Word
from homer.structures.spaces.frame import Frame
from homer.structures.link import Link


class Template(Frame):
    def __init__(
        self,
        members: List[Union[Slot, Word]],
        parent_concept: Concept,
        links_in: List[Link] = None,
        links_out: List[Link] = None,
    ):
        Frame.__init__(
            members,
            parent_concept,
            links_in=links_in,
            links_out=links_out,
        )
