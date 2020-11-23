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
        contents: StructureCollection,
        parent_concept: Concept,
        parent_spaces: StructureCollection = None,
        child_spaces: StructureCollection = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Frame.__init__(
            self,
            name,
            contents,
            parent_concept,
            parent_spaces=parent_spaces,
            child_spaces=child_spaces,
            links_in=links_in,
            links_out=links_out,
        )
