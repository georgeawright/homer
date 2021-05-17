from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ChunkBuilder
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection


class ChunkSelector(Selector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        champion = bubble_chamber.input_nodes.where(is_chunk=True).get_active()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({champion}),
            champion.activation,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

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
        new_target = self.bubble_chamber.chunks.get_unhappy()
        self.child_codelets.append(
            ChunkBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                new_target,
                new_target.unhappiness,
            )
        )

    def _engender_follow_up(self):
        target = self.winners.get_random()
        self.child_codelets.append(
            ChunkBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                target,
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
