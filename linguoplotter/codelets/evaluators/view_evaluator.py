from linguoplotter.codelets.evaluator import Evaluator


class ViewEvaluator(Evaluator):
    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["view"]
        return structure_concept.relations_with(self._evaluate_concept).get()
