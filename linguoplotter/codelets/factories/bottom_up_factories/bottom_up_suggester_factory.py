from linguoplotter.codelets.factories import BottomUpFactory
from linguoplotter.codelets.suggesters import (
    ChunkSuggester,
    CorrespondenceSuggester,
    LabelSuggester,
    RelationSuggester,
)
from linguoplotter.codelets.suggesters import ViewSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero


class BottomUpSuggesterFactory(BottomUpFactory):
    def _engender_follow_up(self):
        proportion_of_unchunked_raw_chunks = self._proportion_of_unchunked_raw_chunks()
        proportion_of_unlabeled_chunks = self._proportion_of_unlabeled_chunks()
        proportion_of_unrelated_chunks = self._proportion_of_unrelated_chunks()
        proportion_of_uncorresponded_links = self._proportion_of_uncorresponded_links()
        proportion_of_unfilled_slots = self._proportion_of_unfilled_slots()

        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Proportion of unchunked raw chunks: {proportion_of_unchunked_raw_chunks}\n"
            + f"Proportion of unlabeled chunks: {proportion_of_unlabeled_chunks}\n"
            + f"Proportion of unrelated chunks: {proportion_of_unrelated_chunks}\n"
            + f"Proportion of uncorresponded links: {proportion_of_uncorresponded_links}\n"
            + f"Proportion of unfilled_slots: {proportion_of_unfilled_slots}",
        )

        follow_up_class = self.bubble_chamber.random_machine.select(
            [
                (ChunkSuggester, proportion_of_unchunked_raw_chunks),
                (LabelSuggester, proportion_of_unlabeled_chunks),
                (RelationSuggester, proportion_of_unrelated_chunks),
                (CorrespondenceSuggester, proportion_of_unfilled_slots),
                (ViewSuggester, proportion_of_uncorresponded_links),
            ],
            key=lambda x: x[1],
        )[0]

        self.child_codelets.append(
            follow_up_class.make(self.codelet_id, self.bubble_chamber)
        )

    def _proportion_of_unchunked_raw_chunks(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        raw_chunks = input_space.contents.filter(
            lambda x: x.is_chunk and x.is_raw
        ).sample(10)
        return len(raw_chunks.where(unchunkedness=1.0)) / len(raw_chunks)

    def _proportion_of_unlabeled_chunks(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            non_raw_chunks = input_space.contents.filter(
                lambda x: x.is_chunk and not x.is_raw
            ).sample(10)
            total_label_quality = sum(
                label.quality for chunk in non_raw_chunks for label in chunk.labels
            )
            return 1 - FloatBetweenOneAndZero(total_label_quality / len(non_raw_chunks))
        except MissingStructureError:
            return float("-inf")

    def _proportion_of_unrelated_chunks(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            non_raw_chunks = input_space.contents.filter(
                lambda x: x.is_chunk and not x.is_raw
            ).sample(10)
            unrelated_non_raw_chunks = non_raw_chunks.filter(
                lambda x: x.relations.is_empty()
            )
            return len(unrelated_non_raw_chunks) / len(non_raw_chunks)
        except MissingStructureError:
            return float("-inf")

    def _proportion_of_uncorresponded_links(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            labels_and_relations = input_space.contents.filter(
                lambda x: x.is_label or x.is_relation
            ).sample(10)
            uncorresponded_links = labels_and_relations.filter(
                lambda x: x.correspondences.is_empty()
            )
            return len(uncorresponded_links) / len(labels_and_relations)
        except MissingStructureError:
            return float("-inf")

    def _proportion_of_unfilled_slots(self):
        try:
            views = self.bubble_chamber.views.sample(10)
            unfilled_slots = sum(len(view.unfilled_input_structures) for view in views)
            slots = sum(
                len(view.parent_frame.input_space.contents.where(is_link=True))
                for view in views
            )
            return unfilled_slots / slots
        except MissingStructureError:
            return float("-inf")
