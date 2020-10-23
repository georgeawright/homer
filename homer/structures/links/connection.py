from homer.structures.concept import Concept
from homer.structures.link import Link


class Connection(Link):
    def __init__(self, start: Concept, end: Concept):
        links_in = None
        links_out = None
        Link.__init__(start, end, links_in, links_out)
