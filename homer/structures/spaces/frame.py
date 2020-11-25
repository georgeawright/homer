from homer.structure_collection import StructureCollection
from homer.structures import Concept, Space


class Frame(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        contents: StructureCollection,
        parent_concept: Concept,
        parent_spaces: StructureCollection = None,
        child_spaces: StructureCollection = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        quality = None
        Space.__init__(
            self,
            structure_id,
            parent_id,
            name,
            contents,
            quality,
            parent_concept,
            parent_spaces=parent_spaces,
            child_spaces=child_spaces,
            links_in=links_in,
            links_out=links_out,
        )
