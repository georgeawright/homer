from typing import List, Union

from homer.structures import Concept
from homer.structure_collection import StructureCollection
from homer.structures.chunks.slot import Slot
from homer.structures.chunks.word import Word
from homer.structures.spaces.frame import Frame
from homer.structures.link import Link


class Template(Frame):
    def __init__(
        self,
        name: str,
        members: List[Union[Slot, Word]],
        parent_concept: Concept,
        parent_spaces: StructureCollection = None,
        child_spaces: StructureCollection = None,
        links_in: List[Link] = None,
        links_out: List[Link] = None,
    ):
        Frame.__init__(
            name,
            members,
            parent_concept,
            parent_spaces=parent_spaces,
            child_spaces=child_spaces,
            links_in=links_in,
            links_out=links_out,
        )
