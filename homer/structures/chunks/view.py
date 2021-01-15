from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunk import Chunk
from homer.structures.links.correspondence import Correspondence
from homer.structures.space import Space
from homer.structures.spaces import WorkingSpace


class View(Chunk):
    """A chunk of self-consistent correspondences."""

    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        location: Location,
        members: StructureCollection,
        output_space: WorkingSpace,
        quality: FloatBetweenOneAndZero,
    ):
        value = None
        parent_space = location.space
        Chunk.__init__(
            self,
            structure_id,
            parent_id,
            value,
            [location],
            members,
            parent_space,
            quality,
            StructureCollection({parent_space}),
        )
        self.output_space = output_space

    @property
    def size(self):
        return len(self.members)
