from homer.bubble_chamber import BubbleChamber
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.codelets.builder import Builder
from homer.structures import Concept
from homer.structures.chunks import View


class ViewEnlarger(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        structure_concept: Concept,
        bubble_chamber: BubbleChamber,
        target_view: View,
        urgency: float,
    ):
        Builder.__init__(self, codelet_id, parent_id, urgency)
        self.structure_concept = structure_concept
        self.bubble_chamber = bubble_chamber
        self.target_view = target_view

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ""
        structure_concept = bubble_chamber.concepts["view"]
        return cls(
            codelet_id,
            parent_id,
            structure_concept,
            bubble_chamber,
            target_view,
            urgency,
        )

    def _passes_preliminary_checks(self):
        pass

    def _calculate_confidence(self):
        pass

    def _boost_activations(self):
        pass

    def _process_structure(self):
        pass

    def _fizzle(self):
        pass

    def _fail(self):
        pass

    def _engender_follow_up(self):
        pass
