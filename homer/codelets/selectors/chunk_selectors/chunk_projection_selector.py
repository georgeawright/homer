import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders.chunk_builders import ChunkProjectionBuilder
from homer.codelets.selectors import ChunkSelector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection


class ChunkProjectionSelector(ChunkSelector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target_view = bubble_chamber.monitoring_views.get_active()
        target_chunk = (
            target_view.interpretation_space.contents.where(is_chunk=True)
            .where_not(members=StructureCollection())
            .get_random()
        )
        target_correspondence = target_chunk.correspondences_to_space(
            target_view.text_space
        ).get_random()
        target_structures = StructureCollection({target_chunk, target_correspondence})
        urgency = statistics.fmean(
            [structure.activation for structure in target_structures]
        )
        return cls.spawn(parent_id, bubble_chamber, target_structures, urgency)

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
