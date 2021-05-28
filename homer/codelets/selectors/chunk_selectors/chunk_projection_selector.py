from homer.codelets.suggesters.chunk_suggesters import ChunkProjectionSuggester
from homer.codelets.selectors import ChunkSelector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation


class ChunkProjectionSelector(ChunkSelector):
    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            champion_chunk = self.champions.where(is_chunk=True).get()
            challenger_chunk = champion_chunk.nearby().get(key=activation)
            challenger_correspondence = challenger_chunk.correspondences.get()
            self.challengers = StructureCollection(
                {challenger_chunk, challenger_correspondence}
            )
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
        target_view = self.winners.where(is_correspondence=True).get().parent_view
        self.child_codelets.append(
            ChunkProjectionSuggester.make(
                self.codelet_id, self.bubble_chamber, target_view=target_view
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

    @property
    def _champions_size(self):
        return self.champions.where(is_chunk=True).get().size

    @property
    def _challengers_size(self):
        return self.challengers.where(is_chunk=True).get().size
