from homer.structure.concept import Concept
from homer.structure.link import Link


class Correspondence(Link):
    def __init__(
        self,
        start: Structure,
        end: Structure,
        parent_concept: Concept,
        is_positive: bool,
    ):
        links_in = []
        links_out = []
        Link.__init__(self, start, end, links_in, links_out)
        self.parent_concept = parent_concept
        self.is_positive = is_positive
