from homer.structure.concept import Concept
from homer.structure.link import Link


class Relation(Link):
    def __init__(self, start: Structure, end: Structure, parent_concept: Concept):
        links_in = []
        links_out = []
        Link.__init__(self, start, end, links_in, links_out)
        self.parent_concept = parent_concept
