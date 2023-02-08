from linguoplotter.codelets.factories import BottomUpFactory
from linguoplotter.codelets.suggesters import (
    ChunkSuggester,
    CorrespondenceSuggester,
    FrameSuggester,
    LabelSuggester,
    RelationSuggester,
    ViewSuggester,
)
from linguoplotter.codelets.suggesters.label_suggesters import (
    InterspatialLabelSuggester,
)
from linguoplotter.codelets.suggesters.relation_suggesters import (
    InterspatialRelationSuggester,
)
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection_keys import (
    uncorrespondedness,
    unlabeledness,
    unrelatedness,
)
from linguoplotter.structure_collections import StructureSet


class BottomUpSuggesterFactory(BottomUpFactory):
    def _engender_follow_up(self):
        input_unchunkedness = self._unchunkedness_of_raw_chunks()
        input_unlabeledness = self._unlabeledness_of_chunks()
        input_unrelatedness = self._unrelatedness_of_chunks()
        input_uncorrespondedness = self._uncorrespondedness_of_links()
        frames_unfilledness = self._unfilledness_of_slots()
        text_uncohesiveness = self._uncohesiveness_of_texts()
        text_unlabeledness = self._unlabeledness_of_letter_chunks()
        text_unrelatedness = self._unrelatedness_of_letter_chunks()

        self.bubble_chamber.loggers["activity"].log(
            f"Unchunked of raw chunks: {input_unchunkedness}\n"
            + f"Unlabeledness of chunks: {input_unlabeledness}\n"
            + f"Unrelatedness of chunks: {input_unrelatedness}\n"
            + f"Unfilledness of slots: {frames_unfilledness}\n"
            + f"Uncorrespondedness of links: {input_uncorrespondedness}\n"
            + f"Unchohesivenss of texts: {text_uncohesiveness}\n"
            + f"Unlabeledness of letter chunks: {text_unlabeledness}\n"
            + f"Unrelatedness of letter chunks: {text_unrelatedness}",
        )

        follow_up_class = self.bubble_chamber.random_machine.select(
            [
                (ChunkSuggester, input_unchunkedness),
                (LabelSuggester, input_unlabeledness),
                (RelationSuggester, input_unrelatedness),
                (ViewSuggester, input_uncorrespondedness),
                (CorrespondenceSuggester, frames_unfilledness),
                (FrameSuggester, text_uncohesiveness),
                (InterspatialLabelSuggester, text_unrelatedness),
                (InterspatialRelationSuggester, text_unrelatedness),
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

    def _uncohesiveness_of_texts(self):
        try:
            view = self.bubble_chamber.views.filter(
                lambda x: x.unhappiness < self.FLOATING_POINT_TOLERANCE
                and x.parent_frame.parent_concept
                == self.bubble_chamber.concepts["conjunction"]
            ).get()
        except MissingStructureError:
            return float("-inf")
        try:
            return 1 / len(view.secondary_frames)
        except ZeroDivisionError:
            return 1

    def _unlabeledness_of_letter_chunks(self):
        try:
            view = self.bubble_chamber.views.filter(
                lambda x: x.unhappiness < self.FLOATING_POINT_TOLERANCE
                and x.parent_frame.parent_concept.location_in_space(
                    self.bubble_chamber.spaces["grammar"]
                )
                == self.bubble_chamber.concepts["sentence"].location_in_space(
                    self.bubble_chamber.spaces["grammar"]
                )
            ).get()
            letter_chunks = view.output_space.contents.filter(
                lambda x: x.is_letter_chunk
                and x.members.is_empty
                and len(x.parent_spaces.where(is_conceptual_space=True)) > 1
            )
            labels = StructureSet.intersection(
                *[c.labels.where(is_interspatial=True) for c in letter_chunks]
            )
            return 1 - sum([l.quality * l.activation for l in labels]) / len(
                view.output_space.conceptual_spaces
            )
        except MissingStructureError:
            return float("-inf")

    def _unrelatedness_of_letter_chunks(self):
        try:
            views = self.bubble_chamber.views.filter(
                lambda x: x.unhappiness < self.FLOATING_POINT_TOLERANCE
                and x.parent_frame.parent_concept.location_in_space(
                    self.bubble_chamber.spaces["grammar"]
                )
                == self.bubble_chamber.concepts["sentence"].location_in_space(
                    self.bubble_chamber.spaces["grammar"]
                )
            ).sample(2)
            view = views.get()
            letter_chunks = view.output_space.contents.filter(
                lambda x: x.is_letter_chunk
                and x.members.is_empty
                and len(x.parent_spaces.where(is_conceptual_space=True)) > 1
            )
            relations = StructureSet.intersection(
                *[c.relations.where(is_interspatial=True) for c in letter_chunks]
            )
            return 1 - sum([r.quality * r.activation for r in relations]) / len(
                view.output_space.conceptual_spaces
            )
        except MissingStructureError:
            return float("-inf")
