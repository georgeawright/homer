from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structures import Concept, Link, Space


class Relation(Link):
    def __init__(
        self,
        start: Structure,
        end: Structure,
        parent_concept: Concept,
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
    ):
        links_in = []
        links_out = []
        Link.__init__(self, start, end, quality, links_in=links_in, links_out=links_out)
        self.parent_concept = parent_concept
        self.parent_space = parent_space
