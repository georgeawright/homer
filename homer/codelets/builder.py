from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.hyper_parameters import HyperParameters
from homer.structures.nodes import Concept


class Builder(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD
    INITIAL_STRUCTURE_ACTIVATION = HyperParameters.INITIAL_STRUCTURE_ACTIVATION

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.child_structures = None
        self.confidence = 0.0

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        raise NotImplementedError

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        return cls.make(parent_id, bubble_chamber, urgency=urgency)

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

    @property
    def _structure_concept(self):
        raise NotImplementedError

    def _boost_activations(self):
        self._build_concept.boost_activation(1)
        self._structure_concept.boost_activation(1)
        self._parent_link.boost_activation(self.confidence)

    def _decay_activations(self):
        self._build_concept.decay_activation()
        self._parent_link.decay_activation(1 - self.confidence)

    def _passes_preliminary_checks(self):
        raise NotImplementedError

    def _calculate_confidence(self):
        raise NotImplementedError

    def _process_structure(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        follow_up_class = self.get_target_class().get_evaluator_class()
        self.child_codelets.append(
            follow_up_class.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.child_structures,
                self.confidence,
            )
        )

    def _fizzle(self):
        raise NotImplementedError

    def _fail(self):
        raise NotImplementedError
