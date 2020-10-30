from homer.structures.chunk import Chunk
from homer.structures.links.correspondence import Correspondence


class View(Chunk):
    """A chunk of self-consistent correspondences."""

    def __init__(self, members, parent_space):
        value = None
        location = None
        neighbours = None
        Chunk.__init__(self, value, location, members, neighbours, parent_space)
        self.output_space = None

    @property
    def size(self):
        return len(self.members)

    def nearby(self):
        raise NotImplementedError

    def add_member(self, new_member: Correspondence):
        pass
