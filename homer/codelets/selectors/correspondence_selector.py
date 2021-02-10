from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import CorrespondenceBuilder
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structures.links import Correspondence


class CorrespondenceSelector(Selector):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Correspondence,
        urgency: FloatBetweenOneAndZero,
        challenger: Correspondence = None,
    ):
        Selector.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.champion = champion
        self.challenger = challenger

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: Correspondence,
        urgency: FloatBetweenOneAndZero,
        challenger: Correspondence = None,
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
        champion = bubble_chamber.correspondences.get_active()
        return cls.spawn(parent_id, bubble_chamber, champion, champion.activation)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["correspondence"]

    def _passes_preliminary_checks(self):
        if self.challenger is not None:
            return True
        candidates = self.champion.start.correspondences_to_space(
            self.champion.end_space
        )
        if len(candidates) > 1:
            self.challenger = candidates.get_active(exclude=[self.champion])
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        try:
            new_target = self.champion.nearby().get_exigent()
            new_target_space = new_target.parent_spaces.where(
                is_basic_level=True
            ).get_random()
        except MissingStructureError:
            return
        self.child_codelets.append(
            CorrespondenceBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                new_target_space,
                new_target,
                new_target.unlinkedness,
            )
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winner,
                self.follow_up_urgency,
                challenger=self.loser,
            )
        )
