from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders.chunk_builders import ChunkProjectionBuilder
from homer.codelets.selectors import ChunkSelector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection


class ChunkProjectionSelector(ChunkSelector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        raise NotImplementedError

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            champion_chunk = self.champions.get_random()
            challenger_chunk = champion_chunk.nearby().get_active()
            self.challengers = StructureCollection({challenger_chunk})
        except MissingStructureError:
            return True
        members_intersection = StructureCollection.intersection(
            champion_chunk.members, challenger_chunk.members
        )
        if not (
            len(members_intersection) > 0.5 * len(champion_chunk.members)
            and len(members_intersection) > 0.5 * len(challenger_chunk.members)
        ):
            self.challengers = None
        return True

    def _fizzle(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        self.child_codelets.append(
            ChunkProjectionBuilder.make(
                self.codelet_id,
                self.bubble_chamber,
            )
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            )
        )
