from abc import abstractmethod, abstractproperty

from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.hyper_parameters import HyperParameters


class Builder(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self, codelet_id: str, parent_id: str, urgency: FloatBetweenOneAndZero
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.confidence = 0.0

    def run(self) -> CodeletResult:
        if not self._passes_preliminary_checks():
            self._parent_link.decay_activation(1 - self.confidence)
            self.bubble_chamber.logger.log(self._parent_link)
            self._fizzle()
            self.result = CodeletResult.FIZZLE
            return self.result
        self._calculate_confidence()
        if abs(self.confidence) > self.CONFIDENCE_THRESHOLD:
            self._parent_link.boost_activation(self.confidence)
            self.bubble_chamber.logger.log(self._parent_link)
            self._process_structure()
            self._engender_follow_up()
            self.result = CodeletResult.SUCCESS
            return self.result
        self._parent_link.decay_activation(1 - self.confidence)
        self.bubble_chamber.logger.log(self._parent_link)
        self._fail()
        self.result = CodeletResult.FAIL
        return CodeletResult.FAIL

    @abstractproperty
    def _parent_link(self):
        pass

    @abstractmethod
    def _passes_preliminary_checks(self):
        pass

    @abstractmethod
    def _calculate_confidence(self):
        pass

    @abstractmethod
    def _process_structure(self):
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
