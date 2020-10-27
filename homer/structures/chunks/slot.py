from homer.location import Location
from homer.structures.chunk import Chunk


class Slot(Chunk):
    """A piece of a frame which acts as a replaceable prototype"""

    def __init__(
        self,
        value: Any = None,
        location: Location = None,
        members: List[Slot] = None,
        neighbours: List[Slot] = None,
        links_in: List[Link] = None,
        links_out: List[Link] = None,
    ):
        Chunk.__init__(self, value, location, members, neighbours, links_in, links_out)
