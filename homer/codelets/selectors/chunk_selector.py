from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ChunkBuilder
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Space


class ChunkSelector(Selector):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_space: Space,
        champion: Chunk,
        urgency: FloatBetweenOneAndZero,
        challenger: Chunk = None,
    ):
        Selector.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.target_space = target_space
        self.champion = champion
        self.challenger = challenger

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_space: Space,
        champion: Chunk,
        urgency: FloatBetweenOneAndZero,
        challenger: Chunk = None,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_space,
            champion,
            urgency,
            challenger=challenger,
        )

    def _passes_preliminary_checks(self):
        if self.challenger is not None:
            return True
        self.challenger = self.champion.nearby(self.target_space).get_active()
        members_intersection = StructureCollection.intersection(
            self.champion.members, self.challenger.members
        )
        return len(members_intersection) > 0.5 * len(self.champion.members) and len(
            members_intersection
        ) > 0.5 * len(self.challenger.members)

    def _boost_winner(self):
        self.winner.boost_activation(self.confidence)

    def _decay_loser(self):
        self.loser.decay_activation(self.confidence)

    def _fizzle(self):
        new_target = self.champion.nearby(self.target_space).get_unhappy()
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
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_space,
                self.champion,
                1 - abs(self.winner.activation - self.loser.activation),
                challenger=self.challenger,
            )
        )
