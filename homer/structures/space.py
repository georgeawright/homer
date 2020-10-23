from homer.structure import Structure


class Space(Structure):
    def __init__(self, contents: list, links_in: list, links_out: list):
        Structure.__init__(self, None, links_in, links_out)
        self.contents = contents
