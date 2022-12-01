from linguoplotter.codelets.factories import BottomUpFactory
from linguoplotter.codelets.suggesters import (
    ChunkSuggester,
    CorrespondenceSuggester,
    LabelSuggester,
    RelationSuggester,
)
from linguoplotter.codelets.suggesters import ViewSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection_keys import (
    uncorrespondedness,
    unlabeledness,
    unrelatedness,
)
from linguoplotter.structure_collections import StructureSet


class BottomUpSuggesterFactory(BottomUpFactory):
    def _engender_follow_up(self):
        chamber_unchunkedness = self._unchunkedness_of_raw_chunks()
        chamber_unlabeledness = self._unlabeledness_of_chunks()
        chamber_unrelatedness = self._unrelatedness_of_chunks()
        chamber_uncorrespondedness = self._uncorrespondedness_of_links()
        chamber_unfilledness = self._unfilledness_of_slots()

        self.bubble_chamber.loggers["activity"].log(
            f"Unchunked of raw chunks: {chamber_unchunkedness}\n"
            + f"Unlabeledness of chunks: {chamber_unlabeledness}\n"
            + f"Unrelatedness of chunks: {chamber_unrelatedness}\n"
            + f"Unfilledness of slots: {chamber_unfilledness}\n"
            + f"Uncorrespondedness of links: {chamber_uncorrespondedness}",
        )

        follow_up_class = self.bubble_chamber.random_machine.select(
            [
                (ChunkSuggester, chamber_unchunkedness),
                (LabelSuggester, chamber_unlabeledness),
                (RelationSuggester, chamber_unrelatedness),
                (ViewSuggester, chamber_uncorrespondedness),
                (CorrespondenceSuggester, chamber_unfilledness),
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
            chunk = input_space.contents.where(is_chunk=True, is_raw=False).get(
                key=unlabeledness
            )
            return 1 - sum([l.quality * l.activation for l in chunk.labels]) / len(
                input_space.conceptual_spaces
            )
        except MissingStructureError:
            return float("-inf")

    def _unrelatedness_of_chunks(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            chunks = input_space.contents.where(is_chunk=True, is_raw=False).sample(
                2, key=unrelatedness
            )
            relations = StructureSet.intersection(*[c.relations for c in chunks])
            return 1 - sum([r.quality * r.activation for r in relations]) / len(
                input_space.conceptual_spaces
            )
        except MissingStructureError:
            return float("-inf")

    def _uncorrespondedness_of_links(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            labels_and_relations = input_space.contents.filter(
                lambda x: x.is_label or x.is_relation
            ).sample(10, key=uncorrespondedness)
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
