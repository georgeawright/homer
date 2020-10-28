from abc import abstractmethod

from homer.codelet import Codelet
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.hyper_parameters import HyperParameters


class Builder(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self, codelet_id: str, parent_id: str, urgency: FloatBetweenOneAndZero
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)

    def run(self):
        if not self._passes_preliminary_checks():
            return self._fizzle()
        self._calculate_confidence()
        if abs(self.confidence) > self.CONFIDENCE_THRESHOLD:
            self._boost_activations()
            self._process_perceptlet()
            return self._engender_follow_up()
        return self._fail()

    @abstractmethod
    def _passes_preliminary_checks(self):
        pass

    @abstractmethod
    def _calculate_confidence(self):
        pass

    @abstractmethod
    def _boost_activations(self):
        pass

    @abstractmethod
    def _process_perceptlet(self):
        pass

    @abstractmethod
    def _engender_follow_up(self):
        pass

    @abstractmethod
    def _fizzle(self):
        pass

    @abstractmethod
    def _fail(self):
        pass
