from homer.structure.concept import Concept
from homer.structure.link import Link


class Label(Link):
    def __init__(self, start: Structure, parent_concept: Concept):
        end = None
        links_in = []
        links_out = []
        Link.__init__(self, start, end, links_in, links_out)
        self.parent_concept = parent_concept
