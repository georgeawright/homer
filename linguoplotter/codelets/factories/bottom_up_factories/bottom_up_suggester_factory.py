from linguoplotter.codelets.factories import BottomUpFactory
from linguoplotter.codelets.suggesters import (
    ChunkSuggester,
    CorrespondenceSuggester,
    LabelSuggester,
    RelationSuggester,
    ViewSuggester,
)
from linguoplotter.codelets.suggesters.label_suggesters import (
    CrossViewLabelSuggester,
)
from linguoplotter.codelets.suggesters.relation_suggesters import (
    CrossViewRelationSuggester,
)
from linguoplotter.codelets.suggesters.view_suggester import (
    BottomUpCohesionViewSuggester,
)
from linguoplotter.codelets.suggesters.view_suggesters import MergedFrameViewSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collection_keys import activation
from linguoplotter.structure_collections import StructureSet


class BottomUpSuggesterFactory(BottomUpFactory):
    def _engender_follow_up(self):
        input_unchunkedness = self._unchunkedness_of_raw_chunks()
        input_unlabeledness = self._unlabeledness_of_chunks()
        input_unrelatedness = self._unrelatedness_of_chunks()
        input_uncorrespondedness = self._uncorrespondedness_of_links()
        frames_unfilledness = self._unfilledness_of_slots()
        cross_view_uncorrespondedness = self._uncorrespondedness_of_cross_view_links()
        text_unlabeledness = self._unlabeledness_of_letter_chunks()
        text_unrelatedness = self._unrelatedness_of_letter_chunks()
        view_unmergedness = self._unmergedness_of_views()

        self.bubble_chamber.loggers["activity"].log(
            f"Unchunkedness of raw chunks: {input_unchunkedness}",
        ).log(
            f"Unlabeledness of chunks: {input_unlabeledness}",
        ).log(
            f"Unrelatedness of chunks: {input_unrelatedness}",
        ).log(
            f"Unfilledness of slots: {frames_unfilledness}",
        ).log(
            f"Uncorrespondedness of links: {input_uncorrespondedness}",
        ).log(
            f"Uncorrespondedness of cross view links: {cross_view_uncorrespondedness}",
        ).log(
            f"Unlabeledness of letter chunks: {text_unlabeledness}",
        ).log(
            f"Unrelatedness of letter chunks: {text_unrelatedness}",
        ).log(
            f"Unmergedness of views: {view_unmergedness}",
        )

        class_urgencies = [
            (ChunkSuggester, input_unchunkedness),
            (LabelSuggester, input_unlabeledness),
            (RelationSuggester, input_unrelatedness),
            (ViewSuggester, input_uncorrespondedness),
            (CorrespondenceSuggester, frames_unfilledness),
            (BottomUpCohesionViewSuggester, cross_view_uncorrespondedness),
            (CrossViewLabelSuggester, text_unrelatedness),
            (CrossViewRelationSuggester, text_unrelatedness),
            (MergedFrameViewSuggester, view_unmergedness),
        ]

        follow_up_class = self.bubble_chamber.random_machine.select(
            class_urgencies, key=lambda x: x[1]
        )[0]

        self.most_urgent_class_urgency = FloatBetweenOneAndZero(
            max(x[1] for x in class_urgencies)
        )

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
                key=activation
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
                2, key=activation
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
                lambda x: x.is_label
                or x.is_relation
                and x.is_fully_active
                and x.quality > 0
            ).sample(len(input_space.conceptual_spaces), key=lambda x: x.quality)
            uncorresponded_links = labels_and_relations.filter(
                lambda x: x.correspondences.is_empty
            )
            return sum(link.quality for link in uncorresponded_links) / len(
                labels_and_relations
            )
        except (ZeroDivisionError, MissingStructureError):
            return float("-inf")

    def _unfilledness_of_slots(self):
        try:
            views = self.bubble_chamber.views.sample(10, key=activation)
            unfilled_slots = sum(view.number_of_items_left_to_process for view in views)
            slots = sum(
                len(view.members) + view.number_of_items_left_to_process
                for view in views
            )
            return unfilled_slots / slots
        except MissingStructureError:
            return float("-inf")

    def _uncorrespondedness_of_cross_view_links(self):
        try:
            sentence_views = self.bubble_chamber.views.filter(
                lambda x: x.unhappiness < self.FLOATING_POINT_TOLERANCE
                and x.parent_frame.parent_concept.location_in_space(
                    self.bubble_chamber.spaces["grammar"]
                )
                == self.bubble_chamber.concepts["sentence"].location_in_space(
                    self.bubble_chamber.spaces["grammar"]
                )
            )
            cross_view_relations = self.bubble_chamber.cross_view_relations.filter(
                lambda x: x.is_fully_active and x.quality > 0
            ).sample(len(sentence_views), key=lambda x: x.quality)
            uncorresponded_relations = cross_view_relations.filter(
                lambda x: x.correspondences.is_empty
            )
            return sum(r.quality for r in uncorresponded_relations) / len(
                cross_view_relations
            )
        except (ZeroDivisionError, MissingStructureError):
            return float("-inf")

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
            ).get(key=activation)
            letter_chunks = view.output_space.contents.filter(
                lambda x: x.is_letter_chunk
                and not x.is_slot
                and x.members.is_empty
                and len(x.parent_spaces.where(is_conceptual_space=True)) > 1
            )
            labels = StructureSet.intersection(
                *[c.labels.where(is_cross_view=True) for c in letter_chunks]
            )
            return 1 - sum([l.quality * l.activation for l in labels]) / len(
                view.output_space.conceptual_spaces
            )
        except MissingStructureError:
            return float("-inf")

    def _unrelatedness_of_letter_chunks(self):
        return self.bubble_chamber.unrelatedness_of_letter_chunks

    def _unmergedness_of_views(self):
        number_of_merged_frame_views = len(
            self.bubble_chamber.views.filter(
                lambda x: x.parent_frame.progenitor.is_merged_frame
            )
        )
        number_of_views_with_mergeable_frames = len(
            self.bubble_chamber.views.filter(
                lambda x: x.unhappiness < self.FLOATING_POINT_TOLERANCE
                and x.parent_frame.progenitor.relations.where(
                    parent_concept=self.bubble_chamber.concepts["more"],
                    conceptual_space=self.bubble_chamber.spaces["grammar"],
                ).not_empty
            )
        )
        try:
            return 1 - (
                number_of_merged_frame_views / number_of_views_with_mergeable_frames
            )
        except ZeroDivisionError:
            return float("-inf")
