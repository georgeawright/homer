from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structure_collection import StructureCollection


class Link(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        start: Structure,
        end: Structure,
        parent_concept: "Concept",
        parent_space: "Space",
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            start.location,
            quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.start = start
        self.end = end
        self.parent_concept = parent_concept
        self.value = parent_concept.name if hasattr(parent_concept, "name") else None
        self.parent_space = parent_space
        self.parent_spaces = StructureCollection({parent_space})

    def copy(
        self, old_arg: Structure = None, new_arg: Structure = None, parent_id: str = ""
    ):
        raise NotImplementedError

    def is_between(self, a: Structure, b: Structure):
        return self.start == a and self.end == b or self.end == a and self.start == a

    def spread_activation(self):
        if not self.is_fully_active():
            return
        if self.parent_concept is not None:
            self.parent_concept.boost_activation()
