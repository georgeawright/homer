from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
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
        except MissingStructureError:
            return self.run()
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                1 - self.bubble_chamber.satisfaction,
            )
        )
        self.result = CodeletResult.SUCCESS
        return self.result

    def _engender_follow_up(self):
        raise NotImplementedError

    def _get_follow_up_type(
        self, action: Concept, structure: Concept, space: Concept, direction: Concept
    ):
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
                        "relation": RelationProjectionSelector,
                        "word": WordSelector,
                    },
                    "reverse": {
                        "chunk": ReverseChunkProjectionSelector,
                    },
                },
            },
        }[action.name][space.name][direction.name][structure.name]

    def codelet_themes(self):
        actions = ["build", "evaluate", "select"]
        return {
            "inner-or-outer": {
                "action": actions,
                "space": ["inner", "outer"],
                "direction": ["forward"],
                "structure": ["chunk", "label", "relation"],
            },
            "inner": {
                "action": actions,
                "space": ["inner"],
                "direction": ["forward"],
                "structure": [
                    "phrase",
                    "correspondence",
                    "view-monitoring",
                    "view-simplex",
                ],
            },
            "outer": {
                "action": actions,
                "space": ["outer"],
                "direction": ["forward"],
                "structure": ["word"],
            },
            "reverse": {
                "action": actions,
                "space": ["outer"],
                "direction": ["reverse"],
                "structure": ["chunk"],
            },
        }
