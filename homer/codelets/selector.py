from abc import abstractmethod

from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.float_between_one_and_zero import FloatBetweenOneAndZero


class Selector(Codelet):
    def __init__(
        self, codelet_id: str, parent_id: str, urgency: FloatBetweenOneAndZero
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.winner = None
        self.loser = None
        self.confidence = 0.0

    def run(self) -> CodeletResult:
        if not self._passes_preliminary_checks():
            self._fizzle()
            self.result = CodeletResult.FIZZLE
            return self.result
        self._hold_competition()
        self._boost_winner()
        self._decay_loser()
        self._engender_follow_up()
        self.result = CodeletResult.SUCCESS
        return self.result

    @abstractmethod
    def _passes_preliminary_checks(self):
        pass

    @abstractmethod
    def _hold_competition(self):
        pass

    @abstractmethod
    def _boost_winner(self):
        pass

    @abstractmethod
    def _decay_loser(self):
        pass

    @abstractmethod
    def _fizzle(self):
        pass

    @abstractmethod
    def _engender_follow_up(self):
        pass
