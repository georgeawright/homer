import statistics

from linguoplotter.codelets.evaluators import (
    ChunkEvaluator,
    LabelEvaluator,
    RelationEvaluator,
)
from linguoplotter.codelets.evaluators.view_evaluators import SimplexViewEvaluator
from linguoplotter.codelets.factories import BottomUpFactory
from linguoplotter.errors import MissingStructureError


class BottomUpEvaluatorFactory(BottomUpFactory):
    def _engender_follow_up(self):
        views_per_frame_type_per_chunk = self._views_per_frame_type_per_chunk()
        relations_per_space_per_end_per_chunk = (
            self._relations_per_space_per_end_per_chunk()
        )
        labels_per_space_per_chunk = self._labels_per_space_per_chunk()
        super_chunks_per_raw_chunk = self._super_chunks_per_raw_chunk()

        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Views per frame type per chunk: {views_per_frame_type_per_chunk}",
        )
        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Relations per space per end per chunk: {relations_per_space_per_end_per_chunk}",
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Labels per space per chunk: {labels_per_space_per_chunk}"
        )
        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Super chunks per raw chunk: {super_chunks_per_raw_chunk}",
        )

        if views_per_frame_type_per_chunk > relations_per_space_per_end_per_chunk:
            follow_up_class = SimplexViewEvaluator
        elif relations_per_space_per_end_per_chunk > labels_per_space_per_chunk:
            follow_up_class = RelationEvaluator
        elif labels_per_space_per_chunk > super_chunks_per_raw_chunk:
            follow_up_class = LabelEvaluator
        else:
            follow_up_class = ChunkEvaluator

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
            if chunks.is_empty():
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
            if chunks.is_empty():
                return 0
        return statistics.fmean(
            [
                (
                    len(chunk.relations)
                    / len([relation.conceptual_space for relation in chunk.relations])
                    / len(chunk.relatives)
                )
                if not chunk.relations.is_empty()
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
            view_types = self.bubble_chamber.new_structure_collection(
                *[view.parent_frame.parent_concept for view in view_sample]
            )
            return len(views) / len(non_raw_chunks)
        except MissingStructureError:
            return 0
        return len(views) / len(view_types) / len(non_raw_chunks)
