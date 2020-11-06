from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures.chunk import Chunk
from homer.structures.links.correspondence import Correspondence
from homer.structures.space import Space


class View(Chunk):
    """A chunk of self-consistent correspondences."""

    def __init__(
        self,
        members: StructureCollection,
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
    ):
        value = None
        location = None
        neighbours = None
        Chunk.__init__(
            self, value, location, members, neighbours, parent_space, quality
        )
        self.output_space = None

    @property
    def size(self):
        return len(self.members)

    def nearby(self):
        raise NotImplementedError

    def add_member(self, new_member: Correspondence):
        pass
