from homer.structures.space import Space


class Frame(Space):
    def __init__(self, contents: list, links_in: list, links_out: list):
        Space.__init__(self, contents, links_in, links_out)
