from linguoplotter.codelets.evaluator import Evaluator


class ProjectionEvaluator(Evaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        raise NotImplementedError

    @property
    def _parent_link(self):
        raise NotImplementedError

    def _calculate_confidence(self):
        raise NotImplementedError
