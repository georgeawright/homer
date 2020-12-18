from typing import List

from homer.location import Location
from homer.structures import Concept, Space
from homer.structure_collection import StructureCollection
from homer.structures.chunks.slot import Slot
from homer.structures.chunks.word import Word
from homer.structures.spaces.frame import Frame
from homer.structures.link import Link


class Template(Frame):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        locations: List[Location],
        contents: StructureCollection,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Frame.__init__(
            self,
            structure_id,
            parent_id,
            name,
            parent_concept,
            locations,
            contents,
            links_in=links_in,
            links_out=links_out,
        )
