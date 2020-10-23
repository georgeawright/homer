from homer.structures.chunk import Chunk


class Text(Chunk):
    def __init__(self, members: List[Structure]):
        value = " ".join(member.value for member in members)
        neighbours = []
        Chunk.__init__(value, members, neighbours)
