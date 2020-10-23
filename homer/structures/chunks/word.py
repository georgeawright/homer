from homer.location import Location
from homer.structures.chunk import Chunk


class Word(Chunk):
    def __init__(
        self,
        value: str,
        location: Location,
        links_in: list = None,
        links_out: list = None,
    ):
        members = []
        neighbours = []
        links_in = [] if links_in is None else links_in
        links_out = [] if links_in is None else links_out
        Chunk.__init__(self, value, location, members, neighbours)
