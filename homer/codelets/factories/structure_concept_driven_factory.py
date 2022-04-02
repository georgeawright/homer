from homer.bubble_chamber import BubbleChamber
from homer.codelets import Factory
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection_keys import activation, exigency, unhappiness


class StructureConceptDrivenFactory(Factory):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
        link_key: callable = lambda x: 0,
        node_key: callable = lambda x: 0,
    ):
        Factory.__init__(self, codelet_id, parent_id, bubble_chamber, coderack, urgency)
        self.link_key = link_key
        self.node_key = node_key

    def follow_up_urgency(self) -> FloatBetweenOneAndZero:
        urgency = 1 - self.bubble_chamber.satisfaction
        if urgency > self.coderack.MINIMUM_CODELET_URGENCY:
            return urgency
        return self.coderack.MINIMUM_CODELET_URGENCY

    def _engender_follow_up(self):
        follow_up_class = self._decide_follow_up_class()
        self.bubble_chamber.loggers["activity"].log(
            self, f"Follow-up class: {follow_up_class.__name__}"
        )
        follow_up = follow_up_class.make(self.codelet_id, self.bubble_chamber)
        self.child_codelets.append(follow_up)

    def _decide_follow_up_class(self):
        from homer.codelets.suggesters import (
            ChunkSuggester,
            CorrespondenceSuggester,
            LabelSuggester,
            RelationSuggester,
        )
        from homer.codelets.suggesters.projection_suggesters import (
            ChunkProjectionSuggester,
            LabelProjectionSuggester,
            RelationProjectionSuggester,
            LetterChunkProjectionSuggester,
        )
        from homer.codelets.suggesters.view_suggesters import (
            MonitoringViewSuggester,
            SimplexViewSuggester,
        )
        from homer.codelets.evaluators import (
            ChunkEvaluator,
            CorrespondenceEvaluator,
            LabelEvaluator,
            RelationEvaluator,
        )
        from homer.codelets.evaluators.projection_evaluators import (
            ChunkProjectionEvaluator,
            LabelProjectionEvaluator,
            RelationProjectionEvaluator,
            LetterChunkProjectionEvaluator,
        )
        from homer.codelets.evaluators.view_evaluators import (
            MonitoringViewEvaluator,
            SimplexViewEvaluator,
        )

        suggest = self.bubble_chamber.concepts["suggest"]
        evaluate = self.bubble_chamber.concepts["evaluate"]

        intra = self.bubble_chamber.concepts["inner"]
        inter = self.bubble_chamber.concepts["outer"]

        chunk = self.bubble_chamber.concepts["chunk"]
        letter_chunk = self.bubble_chamber.concepts["letter-chunk"]
        label = self.bubble_chamber.concepts["label"]
        relation = self.bubble_chamber.concepts["relation"]
        correspondence = self.bubble_chamber.concepts["correspondence"]
        view_simplex = self.bubble_chamber.concepts["view-simplex"]
        view_monitoring = self.bubble_chamber.concepts["view-monitoring"]

        suggest_correspondence = suggest.relations.where(end=correspondence).get()
        suggest_view_simplex = suggest.relations.where(end=view_simplex).get()
        suggest_view_monitoring = suggest.relations.where(end=view_monitoring).get()

        evaluate_view_simplex = evaluate.relations.where(end=view_simplex).get()
        evaluate_view_monitoring = evaluate.relations.where(end=view_monitoring).get()

        chunk_intra = chunk.relations.where(end=intra).get()
        label_intra = label.relations.where(end=intra).get()
        relation_intra = relation.relations.where(end=intra).get()

        chunk_inter = chunk.relations.where(end=inter).get()
        letter_chunk_inter = letter_chunk.relations.where(end=inter).get()
        label_inter = label.relations.where(end=inter).get()
        relation_inter = relation.relations.where(end=inter).get()

        activity_concepts = self.bubble_chamber.new_structure_collection(
            suggest, evaluate
        )

        activity_concept = activity_concepts.get(key=self.node_key)
        self.bubble_chamber.loggers["activity"].log(
            self, f"Found activity concept: {activity_concept}"
        )
        if activity_concept == evaluate:
            structure_link = self.bubble_chamber.new_structure_collection(
                evaluate_view_simplex, evaluate_view_monitoring
            ).get(key=self.link_key)
            self.bubble_chamber.loggers["activity"].log(
                self,
                f"Found structure link: {structure_link.start} -> {structure_link.end}",
            )
            return {
                evaluate_view_simplex: SimplexViewEvaluator,
                evaluate_view_monitoring: MonitoringViewEvaluator,
            }[structure_link]

        structure_link = activity_concept.relations.filter(
            lambda x: x.end.parent_space
            == self.bubble_chamber.conceptual_spaces["structure"]
        ).get(key=self.link_key)
        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Found structure link: {structure_link.start} -> {structure_link.end}",
        )
        try:
            return {
                suggest_correspondence: CorrespondenceSuggester,
                suggest_view_simplex: SimplexViewSuggester,
                suggest_view_monitoring: MonitoringViewSuggester,
            }[structure_link]
        except KeyError:
            pass

        space_link = structure_link.end.relations.filter(
            lambda x: x.end.parent_space
            == self.bubble_chamber.conceptual_spaces["space-type"]
        ).get(key=self.link_key)
        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Found space link: {space_link.start} -> {space_link.end}",
        )
        return {
            chunk_intra: ChunkSuggester,
            label_intra: LabelSuggester,
            relation_intra: RelationSuggester,
            chunk_inter: ChunkProjectionSuggester,
            letter_chunk_inter: LetterChunkProjectionSuggester,
            label_inter: LabelProjectionSuggester,
            relation_inter: RelationProjectionSuggester,
        }[space_link]


class RandomStructureConceptDrivenFactory(StructureConceptDrivenFactory):
    def __init__(
        self,
        codelet_id,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        StructureConceptDrivenFactory.__init__(
            self, codelet_id, parent_id, bubble_chamber, coderack, urgency
        )


class ActiveStructureConceptDrivenFactory(StructureConceptDrivenFactory):
    def __init__(
        self,
        codelet_id,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        StructureConceptDrivenFactory.__init__(
            self,
            codelet_id,
            parent_id,
            bubble_chamber,
            coderack,
            urgency,
            node_key=lambda x: x.activation,
            link_key=lambda x: x.end.activation,
        )


class ExigentStructureConceptDrivenFactory(StructureConceptDrivenFactory):
    def __init__(
        self,
        codelet_id,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        StructureConceptDrivenFactory.__init__(
            self,
            codelet_id,
            parent_id,
            bubble_chamber,
            coderack,
            urgency,
            node_key=lambda x: x.exigency,
            link_key=lambda x: x.end.exigency,
        )


class UnhappyStructureConceptDrivenFactory(StructureConceptDrivenFactory):
    def __init__(
        self,
        codelet_id,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        StructureConceptDrivenFactory.__init__(
            self,
            codelet_id,
            parent_id,
            bubble_chamber,
            coderack,
            urgency,
            node_key=lambda x: x.unhappiness,
            link_key=lambda x: x.end.unhappiness,
        )
