from typing import List, Union

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Concept, Word
from homer.structures.spaces import ConceptualSpace, Frame


class Template(Frame):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        conceptual_space: ConceptualSpace,
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
            conceptual_space,
            locations,
            contents,
            links_in=links_in,
            links_out=links_out,
        )

    def __getitem__(self, index: int) -> Word:
        return self.contents.at(Location([[index]], self)).get_random()
