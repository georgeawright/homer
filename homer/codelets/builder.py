from abc import abstractmethod, abstractproperty

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.hyper_parameters import HyperParameters


class Builder(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.confidence = 0.0

    def run(self) -> CodeletResult:
        if not self._passes_preliminary_checks():
            self._decay_activations()
            self._fizzle()
            self.result = CodeletResult.FIZZLE
            return self.result
        self._calculate_confidence()
        if abs(self.confidence) > self.CONFIDENCE_THRESHOLD:
            self._boost_activations()
            self._process_structure()
            self._engender_follow_up()
            self.result = CodeletResult.SUCCESS
            return self.result
        self._decay_activations()
        self._fail()
        self.result = CodeletResult.FAIL
        return CodeletResult.FAIL

    @property
    def _parent_link(self):
        return self._structure_concept.relations_with(self._build_concept).get_random()

    @property
    def _build_concept(self):
        return self.bubble_chamber.concepts["build"]

    @abstractproperty
    def _structure_concept(self):
        pass

    def _boost_activations(self):
        self._build_concept.boost_activation(1)
        self._structure_concept.boost_activation(1)
        self._parent_link.boost_activation(self.confidence)

    def _decay_activations(self):
        self._build_concept.decay_activation()
        self._parent_link.decay_activation(1 - self.confidence)

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
