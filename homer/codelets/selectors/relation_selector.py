from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import RelationBuilder
from homer.codelets.selector import Selector
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structures.links import Relation


class RelationSelector(Selector):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Relation,
        urgency: FloatBetweenOneAndZero,
        challenger: Relation = None,
    ):
        Selector.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.champion = champion
        self.challenger = challenger

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Relation,
        urgency: FloatBetweenOneAndZero,
        challenger: Relation = None,
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

    def _passes_preliminary_checks(self):
        if self.challenger is not None:
            return True
        space = self.champion.parent_space
        candidates = self.champion.start.relations_in_space_with(
            space, self.champion.end
        )
        if len(candidates) == 1:
            return False
        self.challenger = candidates.get_active(exclude=[self.champion])
        return True

    def _boost_winner(self):
        self.winner.boost_activation(self.confidence)

    def _decay_loser(self):
        self.loser.decay_activation(self.confidence)

    def _fizzle(self):
        self.child_codelets.append(
            RelationBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.champion.parent_spaces.get_random(),
                self.champion.start,
                self.champion.start.unhappiness,
            )
        )

    def _engender_follow_up(self):
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.champion,
                1 - abs(self.winner.activation - self.loser.activation),
                challenger=self.challenger,
            )
        )
