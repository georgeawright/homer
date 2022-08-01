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
        correspondences_per_link = self._correspondences_per_link()
        relations_per_space_per_end_per_chunk = (
            self._relations_per_space_per_end_per_chunk()
        )
        labels_per_space_per_chunk = self._labels_per_space_per_chunk()
        super_chunks_per_raw_chunk = self._super_chunks_per_raw_chunk()

        if correspondences_per_link > relations_per_space_per_end_per_chunk:
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
            try:
                chunks = input_space.contents.filter(
                    lambda x: x.is_chunk and not x.is_raw
                )
            except MissingStructureError:
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
            try:
                chunks = input_space.contents.filter(
                    lambda x: x.is_chunk and not x.is_raw
                )
            except MissingStructureError:
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

    def _correspondences_per_link(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            links = input_space.contents.filter(
                lambda x: x.is_label or x.is_relation
            ).sample(10)
        except MissingStructureError:
            return 0
        return statistics.fmean([len(link.correspondences) for link in links])
