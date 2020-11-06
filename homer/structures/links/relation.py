from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structures import Concept
from homer.structures import Link


class Relation(Link):
    def __init__(
        self,
        start: Structure,
        end: Structure,
        parent_concept: Concept,
        quality: FloatBetweenOneAndZero,
    ):
        links_in = []
        links_out = []
        Link.__init__(self, start, end, quality, links_in=links_in, links_out=links_out)
        self.parent_concept = parent_concept
