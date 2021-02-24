from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ChunkBuilder
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.nodes import Chunk


class ChunkSelector(Selector):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Chunk,
        urgency: FloatBetweenOneAndZero,
        challenger: Chunk = None,
    ):
        Selector.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.champion = champion
        self.challenger = challenger

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Chunk,
        urgency: FloatBetweenOneAndZero,
        challenger: Chunk = None,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            champion,
            urgency,
            challenger=challenger,
        )

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        champion = bubble_chamber.chunks.get_active()
        return cls.spawn(parent_id, bubble_chamber, champion, champion.activation)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self):
        if self.challenger is not None:
            return True
        try:
            self.challenger = self.champion.nearby().get_active()
        except MissingStructureError:
            return True
        members_intersection = StructureCollection.intersection(
            self.champion.members, self.challenger.members
        )
        if not (
            len(members_intersection) > 0.5 * len(self.champion.members)
            and len(members_intersection) > 0.5 * len(self.challenger.members)
        ):
            self.challenger = None
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
        self.child_codelets.append(
            ChunkBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winner,
                self.winner.activation,
            )
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winner,
                self.follow_up_urgency,
            )
        )
