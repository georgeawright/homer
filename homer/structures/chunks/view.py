from homer.float_between_one_and_zero import FloatBetweenOneAndZero
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
        members: StructureCollection,
        parent_space: Space,
        output_space: WorkingSpace,
        quality: FloatBetweenOneAndZero,
    ):
        value = None
        location = None
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

    def nearby(self, space: Space = None):
        return StructureCollection.difference(
            StructureCollection.union(*[member.nearby() for member in self.members]),
            self.members,
        )
