from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structures import Concept, Link, Space


class Correspondence(Link):
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

    def nearby(self, space: Space = None):
        """either correspondences in the same spaces as start and end or other correspondences connected to start or end"""
        raise NotImplementedError

    def get_slot_argument(self):
        from homer.structures.chunks import Slot

        if isinstance(self.start, Slot):
            return self.start
        if isinstance(self.end, Slot):
            return self.end
        raise Exception("Correspondence has no slot argument")

    def get_non_slot_argument(self):
        from homer.structures.chunks import Slot

        if not isinstance(self.start, Slot):
            return self.start
        if not isinstance(self.end, Slot):
            return self.end
        raise Exception("Correspondence has no non slot argument")
