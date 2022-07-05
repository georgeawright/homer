from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection import StructureCollection


class Evaluator(Codelet):
    """Evaluates the quality of target_structure and adjusts its quality accordingly."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: StructureCollection,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self._target_structures = target_structures
        self.original_confidence = target_structures.get().quality
        self.confidence = 0
        self.change_in_confidence = 0

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: StructureCollection,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, target_structures, urgency)

    def run(self):
        self.bubble_chamber.loggers["activity"].log_targets_collection(self)
        self.bubble_chamber.loggers["activity"].log(
            self, f"Original confidence: {self.original_confidence}"
        )
        self._calculate_confidence()
        self.bubble_chamber.loggers["activity"].log(
            self, f"Original confidence: {self.original_confidence}"
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Confidence: {self.confidence}"
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Change in confidence: {self.change_in_confidence}"
        )
        for structure in self.target_structures:
            structure.quality = self.confidence
        self._engender_follow_up()
        self.result = CodeletResult.FINISH
        if self.change_in_confidence > 0:
            self._boost_activations()
        else:
            self._decay_activations()
        self.bubble_chamber.loggers["activity"].log_follow_ups(self)
        self.bubble_chamber.loggers["activity"].log_result(self)
        for structure in self.target_structures:
            self.bubble_chamber.loggers["structure"].log(structure)
        return self.result

    @classmethod
    def get_follow_up_class(cls) -> type:
        raise NotImplementedError

    @property
    def _evaluate_concept(self):
        return self.bubble_chamber.concepts["evaluate"]

    @property
    def _parent_link(self):
        raise NotImplementedError

    @property
    def target_structures(self) -> StructureCollection:
        return self._target_structures

    def _boost_activations(self):
        self._evaluate_concept.boost_activation(self.change_in_confidence)
        self._parent_link.boost_activation(self.change_in_confidence)
        self._evaluate_concept.update_activation()
        self._parent_link.update_activation()

    def _decay_activations(self):
        self._evaluate_concept.decay_activation()
        self._parent_link.decay_activation()
        self._evaluate_concept.update_activation()
        self._parent_link.update_activation()

    def _calculate_confidence(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        self.child_codelets.append(
            self.get_follow_up_class().spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_structures,
                self.change_in_confidence,
            )
        )
