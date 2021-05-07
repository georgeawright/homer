import statistics
from typing import List

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.nodes import Concept
from homer.structures.spaces import ConceptualSpace


class Frame(Space):
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
        quality = 1
        sub_spaces = []
        dimensions = []
        Space.__init__(
            self,
            structure_id,
            parent_id,
            name,
            parent_concept,
            locations,
            contents,
            0,
            dimensions,
            sub_spaces,
            quality,
            is_basic_level=False,
            links_in=links_in,
            links_out=links_out,
        )
        self.conceptual_space = conceptual_space
        self.is_frame = True

    def update_activation(self):
        self._activation = (
            statistics.fmean([structure.activation for structure in self.contents])
            if self.contents != []
            else 0.0
        )
