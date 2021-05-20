from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Concept


class Factory(Codelet):
    """Spawns a new codelet and a copy of itself"""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.coderack = coderack

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, coderack, urgency)

    def run(self) -> CodeletResult:
        try:
            self._engender_follow_up()
            self.result = CodeletResult.SUCCESS
        except MissingStructureError:
            self.result = CodeletResult.FAIL
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                1 - self.bubble_chamber.satisfaction,
            )
        )
        return self.result

    def _engender_follow_up(self):
        raise NotImplementedError

    def _get_codelet_type_from_concepts(
        self, action: Concept, structure: Concept, space: Concept, direction: Concept
    ):
        from homer.codelets import Publisher
        from homer.codelets.builders import (
            ChunkBuilder,
            CorrespondenceBuilder,
            LabelBuilder,
            RelationBuilder,
            WordBuilder,
            PhraseBuilder,
        )
        from homer.codelets.builders.chunk_builders import (
            ChunkProjectionBuilder,
            ReverseChunkProjectionBuilder,
        )
        from homer.codelets.builders.label_builders import (
            LabelProjectionBuilder,
        )
        from homer.codelets.builders.phrase_builders import (
            PhraseProjectionBuilder,
        )
        from homer.codelets.builders.relation_builders import (
            RelationProjectionBuilder,
        )
        from homer.codelets.builders.view_builders import (
            MonitoringViewBuilder,
            SimplexViewBuilder,
        )
        from homer.codelets.evaluators import (
            ChunkEvaluator,
            CorrespondenceEvaluator,
            LabelEvaluator,
            RelationEvaluator,
            WordEvaluator,
            PhraseEvaluator,
        )
        from homer.codelets.evaluators.chunk_evaluators import (
            ChunkProjectionEvaluator,
            ReverseChunkProjectionEvaluator,
        )
        from homer.codelets.evaluators.label_evaluators import (
            LabelProjectionEvaluator,
        )
        from homer.codelets.evaluators.phrase_evaluators import (
            PhraseProjectionEvaluator,
        )
        from homer.codelets.evaluators.relation_evaluators import (
            RelationProjectionEvaluator,
        )
        from homer.codelets.evaluators.view_evaluators import (
            MonitoringViewEvaluator,
            SimplexViewEvaluator,
        )
        from homer.codelets.selectors import (
            ChunkSelector,
            CorrespondenceSelector,
            LabelSelector,
            RelationSelector,
            WordSelector,
            PhraseSelector,
        )
        from homer.codelets.selectors.chunk_selectors import (
            ChunkProjectionSelector,
            ReverseChunkProjectionSelector,
        )
        from homer.codelets.selectors.label_selectors import (
            LabelProjectionSelector,
        )
        from homer.codelets.selectors.phrase_selectors import (
            PhraseProjectionSelector,
        )
        from homer.codelets.selectors.relation_selectors import (
            RelationProjectionSelector,
        )
        from homer.codelets.selectors.view_selectors import (
            MonitoringViewSelector,
            SimplexViewSelector,
        )

        return {
            "build": {
                "inner": {
                    "forward": {
                        "chunk": ChunkBuilder,
                        "correspondence": CorrespondenceBuilder,
                        "label": LabelBuilder,
                        "phrase": PhraseBuilder,
                        "relation": RelationBuilder,
                        "view-monitoring": MonitoringViewBuilder,
                        "view-simplex": SimplexViewBuilder,
                    },
                },
                "outer": {
                    "forward": {
                        "chunk": ChunkProjectionBuilder,
                        "label": LabelProjectionBuilder,
                        "phrase": PhraseProjectionBuilder,
                        "relation": RelationProjectionBuilder,
                        "word": WordBuilder,
                    },
                    "reverse": {
                        "chunk": ReverseChunkProjectionBuilder,
                    },
                },
            },
            "evaluate": {
                "inner": {
                    "forward": {
                        "chunk": ChunkEvaluator,
                        "correspondence": CorrespondenceEvaluator,
                        "label": LabelEvaluator,
                        "phrase": PhraseEvaluator,
                        "relation": RelationEvaluator,
                        "view-monitoring": MonitoringViewEvaluator,
                        "view-simplex": SimplexViewEvaluator,
                    },
                },
                "outer": {
                    "forward": {
                        "chunk": ChunkProjectionEvaluator,
                        "label": LabelProjectionEvaluator,
                        "phrase": PhraseProjectionEvaluator,
                        "relation": RelationProjectionEvaluator,
                        "word": WordEvaluator,
                    },
                    "reverse": {
                        "chunk": ReverseChunkProjectionEvaluator,
                    },
                },
            },
            "select": {
                "inner": {
                    "forward": {
                        "chunk": ChunkSelector,
                        "correspondence": CorrespondenceSelector,
                        "label": LabelSelector,
                        "phrase": PhraseSelector,
                        "relation": RelationSelector,
                        "view-monitoring": MonitoringViewSelector,
                        "view-simplex": SimplexViewSelector,
                    },
                },
                "outer": {
                    "forward": {
                        "chunk": ChunkProjectionSelector,
                        "label": LabelProjectionSelector,
                        "phrase": PhraseProjectionSelector,
                        "relation": RelationProjectionSelector,
                        "word": WordSelector,
                    },
                    "reverse": {
                        "chunk": ReverseChunkProjectionSelector,
                    },
                },
            },
            "publish": {
                "publish": {
                    "publish": {
                        "publish": Publisher,
                    }
                }
            },
        }[action.name][space.name][direction.name][structure.name]

    def codelet_themes(self):
        build = self.bubble_chamber.concepts["build"]
        evaluate = self.bubble_chamber.concepts["evaluate"]
        select = self.bubble_chamber.concepts["select"]
        inner = self.bubble_chamber.concepts["inner"]
        outer = self.bubble_chamber.concepts["outer"]
        forward = self.bubble_chamber.concepts["forward"]
        reverse = self.bubble_chamber.concepts["reverse"]
        correspondence = self.bubble_chamber.concepts["correspondence"]
        chunk = self.bubble_chamber.concepts["chunk"]
        label = self.bubble_chamber.concepts["label"]
        phrase = self.bubble_chamber.concepts["phrase"]
        relation = self.bubble_chamber.concepts["relation"]
        view_monitoring = self.bubble_chamber.concepts["view-monitoring"]
        view_simplex = self.bubble_chamber.concepts["view-simplex"]
        word = self.bubble_chamber.concepts["word"]
        publish = self.bubble_chamber.concepts["publish"]
        return {
            "inner-or-outer": {
                "actions": StructureCollection({build, evaluate, select}),
                "spaces": StructureCollection({inner, outer}),
                "directions": StructureCollection({forward}),
                "structures": StructureCollection({chunk, label, phrase, relation}),
            },
            "inner": {
                "actions": StructureCollection({build, evaluate, select}),
                "spaces": StructureCollection({inner}),
                "directions": StructureCollection({forward}),
                "structures": StructureCollection(
                    {correspondence, view_monitoring, view_simplex}
                ),
            },
            "outer": {
                "actions": StructureCollection({build, evaluate, select}),
                "spaces": StructureCollection({outer}),
                "directions": StructureCollection({forward}),
                "structures": StructureCollection({word}),
            },
            "reverse": {
                "actions": StructureCollection({build, evaluate, select}),
                "spaces": StructureCollection({outer}),
                "directions": StructureCollection({reverse}),
                "structures": StructureCollection({chunk}),
            },
            "publish": {
                "actions": StructureCollection({publish}),
                "spaces": StructureCollection({publish}),
                "directions": StructureCollection({publish}),
                "structures": StructureCollection({publish}),
            },
        }
