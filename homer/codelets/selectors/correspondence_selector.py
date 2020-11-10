from homer.codelets.selector import Selector
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID


class CorrespondenceSelector(Selector):
    def __init__(
        self, codelet_id: str, parent_id: str, urgency: FloatBetweenOneAndZero
    ):
        pass

    @classmethod
    def spawn(cls, parent_id: str, urgency: FloatBetweenOneAndZero):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, urgency)

    def _passes_preliminary_checks(self):
        pass

    def _hold_competition(self):
        pass

    def _boost_winner(self):
        pass

    def _decay_loser(self):
        pass

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        pass
