import statistics

from linguoplotter.codelets.factories import BottomUpFactory
from linguoplotter.codelets.suggesters import (
    ChunkSuggester,
    CorrespondenceSuggester,
    LabelSuggester,
    RelationSuggester,
)
from linguoplotter.codelets.suggesters import ViewSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collections import StructureSet


class BottomUpSuggesterFactory(BottomUpFactory):
    def _engender_follow_up(self):
        unchunkedness = self._unchunkedness_of_raw_chunks()
        unlabeledness = self._unlabeledness_of_chunks()
        unrelatedness = self._unrelatedness_of_chunks()
        uncorrespondedness = self._uncorrespondedness_of_links()
        unfilledness = self._unfilledness_of_slots()

        self.bubble_chamber.loggers["activity"].log(
            f"Proportion of unchunked raw chunks: {unchunkedness}\n"
            + f"Proportion of unlabeled chunks: {unlabeledness}\n"
            + f"Proportion of unrelated chunks: {unrelatedness}\n"
            + f"Proportion of uncorresponded links: {uncorrespondedness}\n"
            + f"Proportion of unfilled_slots: {unfilledness}",
        )

        follow_up_class = self.bubble_chamber.random_machine.select(
            [
                (ChunkSuggester, unchunkedness),
                (LabelSuggester, unlabeledness),
                (RelationSuggester, unrelatedness),
                (ViewSuggester, uncorrespondedness),
                (CorrespondenceSuggester, unfilledness),
            ],
            key=lambda x: x[1],
        )[0]

        self.child_codelets.append(
            follow_up_class.make(self.codelet_id, self.bubble_chamber)
        )

    def _unchunkedness_of_raw_chunks(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        raw_chunks = input_space.contents.filter(
            lambda x: x.is_chunk and x.is_raw
        ).sample(10)
        return len(raw_chunks.where(unchunkedness=1.0)) / len(raw_chunks)

    def _unlabeledness_of_chunks(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            chunk = input_space.contents.where(is_chunk=True, is_raw=False).get()
            return 1 - sum([l.quality for l in chunk.labels]) / len(
                input_space.conceptual_spaces
            )
        except MissingStructureError:
            return float("-inf")

    def _unrelatedness_of_chunks(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            chunks = input_space.contents.where(is_chunk=True, is_raw=False).sample(2)
            relations = StructureSet.intersection(*[c.relations for c in chunks])
            return 1 - sum([r.quality for r in relations]) / len(
                input_space.conceptual_spaces
            )
        except MissingStructureError:
            return float("-inf")

    def _uncorrespondedness_of_links(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            labels_and_relations = input_space.contents.filter(
                lambda x: x.is_label or x.is_relation
            ).sample(10)
            uncorresponded_links = labels_and_relations.filter(
                lambda x: x.correspondences.is_empty
            )
            return len(uncorresponded_links) / len(labels_and_relations)
        except MissingStructureError:
            return float("-inf")

    def _unfilledness_of_slots(self):
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
