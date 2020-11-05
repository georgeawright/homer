from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structures import Space


class FunctionWordsBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        input_space: Space,
        output_space: Space,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, urgency)
        pass

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        input_space: Space,
        output_space: Space,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ""
        return cls(codelet_id, parent_id, input_space, output_space, urgency)

    def _passes_preliminary_checks(self):
        pass

    def _boost_activations(self):
        pass

    def _calculate_confidence(self):
        pass

    def _process_structure(self):
        pass

    def _fizzle(self):
        pass

    def _fail(self):
        pass

    def _engender_follow_up(self):
        pass
