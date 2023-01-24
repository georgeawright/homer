import statistics

from linguoplotter.codelets.evaluators import (
    ChunkEvaluator,
    LabelEvaluator,
    RelationEvaluator,
    ViewEvaluator,
)
from linguoplotter.codelets.evaluators.relation_evaluators import (
    InterspatialRelationEvaluator,
)
from linguoplotter.codelets.factories import BottomUpFactory
from linguoplotter.errors import MissingStructureError
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collections import StructureSet


class BottomUpEvaluatorFactory(BottomUpFactory):
    FLOATING_POINT_TOLERANCE = HyperParameters.FLOATING_POINT_TOLERANCE

    def _engender_follow_up(self):
        views_per_frame_type_per_chunk = self._views_per_frame_type_per_chunk()
        relations_per_space_per_end_per_chunk = (
            self._relations_per_space_per_end_per_chunk()
        )
        labels_per_space_per_chunk = self._labels_per_space_per_chunk()
        super_chunks_per_raw_chunk = self._super_chunks_per_raw_chunk()
        related_texts_per_letter_chunk = self._related_texts_per_letter_chunk()

        self.bubble_chamber.loggers["activity"].log(
            f"Views per frame type per chunk: {views_per_frame_type_per_chunk}\n"
            + f"Relations per space per end per chunk: {relations_per_space_per_end_per_chunk}\n"
            + f"Labels per space per chunk: {labels_per_space_per_chunk}\n"
            + f"Super chunks per raw chunk: {super_chunks_per_raw_chunk}\n"
            + f"Related texts per letter chunk: {related_texts_per_letter_chunk}",
        )

        follow_up_class = self.bubble_chamber.random_machine.select(
            [
                (ChunkEvaluator, super_chunks_per_raw_chunk),
                (LabelEvaluator, labels_per_space_per_chunk),
                (RelationEvaluator, relations_per_space_per_end_per_chunk),
                (ViewEvaluator, views_per_frame_type_per_chunk),
                (InterspatialRelationEvaluator, related_texts_per_letter_chunk),
            ],
            key=lambda x: x[1],
        )[0]

        self.child_codelets.append(
            follow_up_class.make(self.codelet_id, self.bubble_chamber)
        )

    def _super_chunks_per_raw_chunk(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        raw_chunks = input_space.contents.filter(
            lambda x: x.is_chunk and x.is_raw
        ).sample(10)
        return statistics.fmean([len(chunk.super_chunks) for chunk in raw_chunks])

    def _labels_per_space_per_chunk(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            chunks = input_space.contents.filter(
                lambda x: x.is_chunk and not x.is_raw
            ).sample(10)
        except MissingStructureError:
            chunks = input_space.contents.filter(lambda x: x.is_chunk and not x.is_raw)
            if chunks.is_empty:
                return 0
        return statistics.fmean(
            [
                len(chunk.labels_in_space(space))
                for chunk in chunks
                for space in chunk.parent_spaces.where(is_conceptual_space=True)
            ]
        )

    def _relations_per_space_per_end_per_chunk(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            chunks = input_space.contents.filter(
                lambda x: x.is_chunk and not x.is_raw
            ).sample(10)
        except MissingStructureError:
            chunks = input_space.contents.filter(lambda x: x.is_chunk and not x.is_raw)
            if chunks.is_empty:
                return 0
        return statistics.fmean(
            [
                (
                    len(chunk.relations)
                    / len([relation.conceptual_space for relation in chunk.relations])
                    / len(chunk.relatives)
                )
                if chunk.relations.not_empty
                else 0
                for chunk in chunks
            ]
        )

    def _views_per_frame_type_per_chunk(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        non_raw_chunks = input_space.contents.where(is_chunk=True, is_raw=False)
        views = self.bubble_chamber.views
        try:
            view_sample = views.sample(10)
            view_types = self.bubble_chamber.new_set(
                *[view.parent_frame.parent_concept for view in view_sample]
            )
            return len(views) / len(non_raw_chunks)
        except MissingStructureError:
            return 0
        return len(views) / len(view_types) / len(non_raw_chunks)

    def _related_texts_per_letter_chunk(self):
        try:
            views = self.bubble_chamber.views.filter(
                lambda x: x.unhappiness < self.FLOATING_POINT_TOLERANCE
                and x.parent_frame.parent_concept
                == self.bubble_chamber.concepts["sentence"]
            ).sample(2)
            view = views.get()
            letter_chunks = view.output_space.contents.filter(
                lambda x: x.is_letter_chunk
                and x.members.is_empty
                and len(x.parent_spaces.where(is_conceptual_space=True)) > 1
            )
            return statistics.fmean(
                [
                    (
                        len(chunk.relations)
                        / len([relative.parent_space for relative in chunk.relatives])
                    )
                    if chunk.relations.not_empty
                    else 0
                    for chunk in letter_chunks
                ]
            )
        except MissingStructureError:
            return 0
