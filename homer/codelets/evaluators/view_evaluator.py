from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator
from homer.structure_collection import StructureCollection


class ViewEvaluator(Evaluator):
    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["view"]
        return structure_concept.relations_with(self._evaluate_concept).get_random()
