from linguoplotter.codelets.factories import BottomUpFactory
from linguoplotter.codelets.suggesters import (
    ChunkSuggester,
    LabelSuggester,
    RelationSuggester,
)
from linguoplotter.codelets.suggesters.view_suggesters import SimplexViewSuggester


class BottomUpSuggesterFactory(BottomUpFactory):
    def _engender_follow_up(self):
        proportion_of_unchunked_raw_chunks = self._proportion_of_unchunked_raw_chunks()
        proportion_of_unlabeled_chunks = self._proportion_of_unlabeled_chunks()
        proportion_of_unrelated_chunks = self._proportion_of_unrelated_chunks()
        proportion_of_uncorresponded_links = self._proportion_of_uncorresponded_links()

        if proportion_of_unchunked_raw_chunks > proportion_of_unlabeled_chunks:
            follow_up_class = ChunkSuggester
        elif proportion_of_unlabeled_chunks > proportion_of_unrelated_chunks:
            follow_up_class = LabelSuggester
        elif proportion_of_unrelated_chunks > proportion_of_uncorresponded_links:
            follow_up_class = RelationSuggester
        else:
            follow_up_class = SimplexViewSuggester

        self.child_codelets.append(
            follow_up_class.make(self.codelet_id, self.bubble_chamber)
        )
