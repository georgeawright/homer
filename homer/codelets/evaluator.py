from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.hyper_parameters import HyperParameters
from homer.id import ID
from homer.structure import Structure


class Evaluator(Codelet):
    """Evaluates the quality of target_structure and adjusts its quality accordingly."""

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structure: Structure,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.target_structure = target_structure
        self.confidence = 0
        self.change_in_confidence = 0

    def run(self):
        self._calculate_confidence()
        self.target_structure.quality = self.confidence
        self._engender_follow_up()
        self.result = CodeletResult.SUCCESS
        if self.change_in_confidence > self.CONFIDENCE_THRESHOLD:
            self._boost_activations()
        else:
            self._decay_activations()
        return self.result

    @property
    def _evaluate_concept(self):
        return self.bubble_chamber.concepts["evaluate"]

    @property
    def _parent_link(self):
        raise NotImplementedError

    def _boost_activations(self):
        self._evaluate_concept.boost_activation(1)
        self._parent_link.boost_activation(self.change_in_confidence)

    def _decay_activations(self):
        self._evaluate_concept.decay_activation()
        self._parent_link.decay_activation()

    def _calculate_confidence(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        selector_class = self.get_target_class().get_selector_class()
        self.child_codelets.append(
            selector_class.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_structure,
                self.change_in_confidence,
            )
        )
