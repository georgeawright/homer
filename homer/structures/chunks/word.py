from homer.structures.chunk import Chunk


class Word(Chunk):
    def __init__(self, value: str):
        members = []
        neighbours = []
        Chunk.__init__(self, value, members, neighbours)
