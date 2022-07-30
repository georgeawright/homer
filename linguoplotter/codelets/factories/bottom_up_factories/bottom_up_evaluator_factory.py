from linguoplotter.codelets.evaluators import (
    ChunkEvaluator,
    LabelEvaluator,
    RelationEvaluator,
)
from linguoplotter.codelets.evaluators.view_evaluators import SimplexViewEvaluator
from linguoplotter.codelets.factories import BottomUpFactory


class BottomUpEvaluatorFactory(BottomUpFactory):
    def _engender_follow_up(self):
        proportion_of_unchunked_raw_chunks = self._proportion_of_unchunked_raw_chunks()
        proportion_of_unlabeled_chunks = self._proportion_of_unlabeled_chunks()
        proportion_of_unrelated_chunks = self._proportion_of_unrelated_chunks()
        proportion_of_uncorresponded_links = self._proportion_of_uncorresponded_links()

        if proportion_of_unchunked_raw_chunks < proportion_of_unlabeled_chunks:
            follow_up_class = ChunkEvaluator
        elif proportion_of_unlabeled_chunks < proportion_of_unrelated_chunks:
            follow_up_class = LabelEvaluator
        elif proportion_of_unrelated_chunks < proportion_of_uncorresponded_links:
            follow_up_class = RelationEvaluator
        else:
            follow_up_class = SimplexViewEvaluator

        self.child_codelets.append(
            follow_up_class.make(self.codelet_id, self.bubble_chamber)
        )
