from homer.structures.chunk import Chunk
from homer.structures.slot import Slot

from .word import Word


class Template(Chunk):
    def __init__(self, members: List[Union[Slot, Word]]):
        value = " ".join(member.value for member in members)
        neighbours = []
        Chunk.__init__(value, members, neighbours)
