from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders.chunk_builders import ReverseChunkProjectionBuilder
from homer.codelets.selectors import ChunkSelector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection


class ReverseChunkProjectionSelector(ChunkSelector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        raise NotImplementedError

    def _passes_preliminary_checks(self):
        return True

    def _fizzle(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        target_view = (
            self.winners.where(is_correspondence=True).get_random().parent_view
        )
        target_interpretation_chunk = StructureCollection(
            {
                chunk
                for chunk in self.winners.where(is_chunk=True)
                if not chunk.members.is_empty()
            }
        ).get_random()
        try:
            target_raw_chunk = (
                target_interpretation_chunk.members.get_random()
                .correspondences_to_space(target_view.raw_input_space)
                .get_random()
                .arguments.where(is_raw=True)
                .get_random()
            )
        except MissingStructureError:
            target_raw_chunk = target_view.raw_input_space.contents.where(
                is_raw=True
            ).get_random()
        target = self.winners.get_random()
        self.child_codelets.append(
            ReverseChunkProjectionBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                target_view,
                target_interpretation_chunk,
                target_raw_chunk,
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
