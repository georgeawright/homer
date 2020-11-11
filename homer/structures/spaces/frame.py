from homer.structure_collection import StructureCollection
from homer.structures import Concept, Space


class Frame(Space):
    def __init__(
        self,
        contents: StructureCollection,
        parent_concept: Concept,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        quality = None
        Space.__init__(
            self,
            contents,
            quality,
            parent_concept,
            links_in=links_in,
            links_out=links_out,
        )
