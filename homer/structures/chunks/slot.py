from homer.structures.chunk import Chunk


class Slot(Chunk):
    """A slot is a piece of a framelet which needs to be filled in with a word.
    prototype - a set of concepts which the filler should belong to.
    form - the orm of the lexeme that the word should use."""

    def __init__(self, prototype):
        self.prototype = prototype
