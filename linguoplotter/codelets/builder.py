from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structures.nodes import Concept


class Builder(Codelet):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.child_structures = None

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

    @classmethod
    def get_follow_up_class(cls) -> type:
        raise NotImplementedError

    def run(self) -> CodeletResult:
        self.bubble_chamber.loggers["activity"].log_targets_dict(self)
        if not self._passes_preliminary_checks():
            self._decay_activations()
            self._fizzle()
            self.result = CodeletResult.FIZZLE
        else:
            self._boost_activations()
            self._process_structure()
            self.bubble_chamber.loggers["activity"].log_child_structures(self)
            self._engender_follow_up()
            self.result = CodeletResult.FINISH
        self.bubble_chamber.loggers["activity"].log_follow_ups(self)
        self.bubble_chamber.loggers["activity"].log_result(self)
        return self.result

    @property
    def _parent_link(self):
        return self._structure_concept.relations_with(self._build_concept).get()

    @property
    def _build_concept(self):
        return self.bubble_chamber.concepts["build"]

    @property
    def _structure_concept(self):
        raise NotImplementedError

    @property
    def target_structures(self):
        return self.bubble_chamber.new_structure_collection(
            *[structure for structure in self._target_structures.values()]
        )

    def _boost_activations(self):
        self._build_concept.boost_activation(1)
        self._structure_concept.boost_activation(1)
        self._parent_link.boost_activation(self.urgency)
        self._build_concept.update_activation()
        self._structure_concept.update_activation()
        self._parent_link.update_activation()

    def _decay_activations(self):
        self._build_concept.decay_activation()
        self._parent_link.decay_activation(1 - self.urgency)
        self._build_concept.update_activation()
        self._parent_link.update_activation()

    def _passes_preliminary_checks(self):
        raise NotImplementedError

    def _process_structure(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        self.child_codelets.append(
            self.get_follow_up_class().spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.child_structures,
                self.urgency,
            )
        )

    def _fizzle(self):
        raise NotImplementedError

    def _fail(self):
        raise NotImplementedError
