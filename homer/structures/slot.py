from homer.structure import Structure


class Slot(Structure):
    """A slot is a piece of a framelet which needs to be filled in with a word.
    prototype - a set of concepts which the filler should belong to.
    form - the form of the lexeme that the word should use."""

    def __init__(self, prototype, form):
        self.prototype = prototype
        self.form = form
