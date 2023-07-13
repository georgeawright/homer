import statistics

from linguoplotter.codelets.evaluators import (
    ChunkEvaluator,
    LabelEvaluator,
    RelationEvaluator,
    ViewEvaluator,
)
from linguoplotter.codelets.evaluators.label_evaluators import (
    CrossViewLabelEvaluator,
)
from linguoplotter.codelets.evaluators.relation_evaluators import (
    CrossViewRelationEvaluator,
)
from linguoplotter.codelets.factories import BottomUpFactory
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collection_keys import activation
from linguoplotter.structure_collections import StructureSet


class BottomUpEvaluatorFactory(BottomUpFactory):
    FLOATING_POINT_TOLERANCE = HyperParameters.FLOATING_POINT_TOLERANCE

    def _engender_follow_up(self):
        chunk_competition = self._chunk_competition()
        label_competition = self._label_competition()
        relation_competition = self._relation_competition()
        view_competition = self._view_competition()
        cross_view_relation_competition = self._cross_view_relation_competition()
        cross_view_label_competition = self._cross_view_label_competition()
        self.bubble_chamber.loggers["activity"].log(
            f"Chunk competition: {chunk_competition}",
        ).log(
            f"Label competition: {label_competition}",
        ).log(
            f"Relation competition: {relation_competition}",
        ).log(
            f"View competition: {view_competition}",
        ).log(
            f"Cross relation competition: {cross_view_relation_competition}",
        ).log(
            f"Cross label competition: {cross_view_label_competition}",
        )
        class_urgencies = [
            (ChunkEvaluator, chunk_competition),
            (LabelEvaluator, label_competition),
            (RelationEvaluator, relation_competition),
            (ViewEvaluator, view_competition),
            (CrossViewRelationEvaluator, cross_view_relation_competition),
            (CrossViewLabelEvaluator, cross_view_label_competition),
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

    def _chunk_competition(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            chunk = input_space.contents.where(is_chunk=True, is_raw=False).get(
                key=activation
            )
            competing_chunks = input_space.contents.filter(
                lambda x: x.is_chunk
                and not x.is_raw
                and x.activation > 0
                and StructureSet.intersection(x.members, chunk.members).not_empty
            )
            return 1 - 0.5 ** len(competing_chunks)
        except MissingStructureError:
            return float("-inf")

    def _label_competition(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            label = input_space.contents.where(is_label=True).get(key=activation)
            competing_labels = label.start.labels.filter(
                lambda x: x.activation > 0 and x.is_competing_with(label)
            )
            return 1 - 0.5 ** len(competing_labels)
        except MissingStructureError:
            return float("-inf")

    def _relation_competition(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            relation = input_space.contents.where(is_relation=True).get()
            competing_relations = relation.start.relations.filter(
                lambda x: x.activation > 0
                and x.start == relation.start
                and x.is_competing_with(relation)
            )
            return 1 - 0.5 ** len(competing_relations)
        except MissingStructureError:
            return float("-inf")

    def _view_competition(self):
        try:
            view = self.bubble_chamber.views.get(key=activation)
            competing_views = self.bubble_chamber.views.filter(
                lambda x: x.activation > 0 and x.is_competing_with(view)
            )
            return 1 - 0.5 ** len(competing_views)
        except MissingStructureError:
            return float("-inf")

    def _cross_view_relation_competition(self):
        try:
            relation = self.bubble_chamber.cross_view_relations.get()
            competing_relations = relation.start.relations.filter(
                lambda x: x.is_cross_view
                and x.activation > 0
                and x.start == relation.start
                and x.is_competing_with(relation)
            )
            return 1 - 0.5 ** len(competing_relations)
        except MissingStructureError:
            return float("-inf")

    def _cross_view_label_competition(self):
        try:
            label = self.bubble_chamber.cross_view_labels.get()
            competing_labels = label.start.labels.filter(
                lambda x: x.is_cross_view
                and x.activation > 0
                and x.is_competing_with(label)
            )
            return 1 - 0.5 ** len(competing_labels)
        except MissingStructureError:
            return float("-inf")
