from homer.codelets.suggesters.chunk_suggesters import ReverseChunkProjectionSuggester
from homer.codelets.selectors import ChunkSelector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection


class ReverseChunkProjectionSelector(ChunkSelector):
    def _passes_preliminary_checks(self):
        return True

    def _fizzle(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        target_view = self.winners.where(is_correspondence=True).get().parent_view
        target_interpretation_chunk = StructureCollection(
            {
                chunk
                for chunk in self.winners.where(is_chunk=True)
                if not chunk.members.is_empty()
            }
        ).get()
        try:
            target_raw_chunk = (
                target_interpretation_chunk.members.get()
                .correspondences_to_space(target_view.raw_input_space)
                .get()
                .arguments.where(is_raw=True)
                .get()
            )
        except MissingStructureError:
            target_raw_chunk = target_view.raw_input_space.contents.where(
                is_raw=True
            ).get()
        target = self.winners.get()
        self.child_codelets.append(
            ReverseChunkProjectionSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {
                    "target_view": target_view,
                    "target_interpretation_chunk": target_interpretation_chunk,
                    "target_raw_chunk": target_raw_chunk,
                },
                target.activation,
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
