from homer.structure import Structure
from homer.structures import Concept
from homer.structures import Link


class Correspondence(Link):
    def __init__(
        self,
        start: Structure,
        end: Structure,
        parent_concept: Concept,
    ):
        links_in = []
        links_out = []
        Link.__init__(self, start, end, links_in, links_out)
        self.parent_concept = parent_concept

    def nearby(self):
        """either correspondences in the same spaces as start and end or other correspondences connected to start or end"""
        raise NotImplementedError
