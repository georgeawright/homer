from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structures.nodes import Concept

# TODO: also need to implement instances based on bubble chamber structures
# definitely: unhappiness and exigency
# possibly: activation and quality


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
        from homer.codelets.suggesters import (
            ChunkSuggester,
            LabelSuggester,
            RelationSuggester,
        )
        from homer.codelets.suggesters.correspondence_suggesters import (
            SpaceToFrameCorrespondenceSuggester,
            SubFrameToFrameCorrespondenceSuggester,
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

        return {
            "suggest": {
                "inner": {
                    "forward": {
                        "chunk": ChunkSuggester,
                        "correspondence": SpaceToFrameCorrespondenceSuggester,
                        "label": LabelSuggester,
                        "relation": RelationSuggester,
                        "view-monitoring": MonitoringViewSuggester,
                        "view-simplex": SimplexViewSuggester,
                    },
                },
                "outer": {
                    "forward": {
                        "chunk": ChunkProjectionSuggester,
                        "correspondence": SubFrameToFrameCorrespondenceSuggester,
                        "label": LabelProjectionSuggester,
                        "relation": RelationProjectionSuggester,
                        "letter-chunk": LetterChunkProjectionSuggester,
                    },
                },
            },
            "evaluate": {
                "inner": {
                    "forward": {
                        "chunk": ChunkEvaluator,
                        "correspondence": CorrespondenceEvaluator,
                        "label": LabelEvaluator,
                        "relation": RelationEvaluator,
                        "view-monitoring": MonitoringViewEvaluator,
                        "view-simplex": SimplexViewEvaluator,
                    },
                },
                "outer": {
                    "forward": {
                        "chunk": ChunkProjectionEvaluator,
                        "correspondence": CorrespondenceEvaluator,
                        "label": LabelProjectionEvaluator,
                        "relation": RelationProjectionEvaluator,
                        "letter-chunk": LetterChunkProjectionEvaluator,
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
        suggest = self.bubble_chamber.concepts["suggest"]
        evaluate = self.bubble_chamber.concepts["evaluate"]
        publish = self.bubble_chamber.concepts["publish"]
        inner = self.bubble_chamber.concepts["inner"]
        outer = self.bubble_chamber.concepts["outer"]
        forward = self.bubble_chamber.concepts["forward"]
        correspondence = self.bubble_chamber.concepts["correspondence"]
        chunk = self.bubble_chamber.concepts["chunk"]
        label = self.bubble_chamber.concepts["label"]
        relation = self.bubble_chamber.concepts["relation"]
        view_monitoring = self.bubble_chamber.concepts["view-monitoring"]
        view_simplex = self.bubble_chamber.concepts["view-simplex"]
        letter_chunk = self.bubble_chamber.concepts["letter-chunk"]

        nsc = lambda *x: self.bubble_chamber.new_structure_collection(*x)

        return {
            "inner-or-outer": {
                "actions": nsc(suggest, evaluate),
                "spaces": nsc(inner, outer),
                "directions": nsc(forward),
                "structures": nsc(chunk, correspondence, label, relation),
            },
            "inner": {
                "actions": nsc(suggest, evaluate),
                "spaces": nsc(inner),
                "directions": nsc(forward),
                "structures": nsc(view_monitoring, view_simplex),
            },
            "outer": {
                "actions": nsc(suggest, evaluate),
                "spaces": nsc(outer),
                "directions": nsc(forward),
                "structures": nsc(letter_chunk),
            },
            "publish": {
                "actions": nsc(publish),
                "spaces": nsc(publish),
                "directions": nsc(publish),
                "structures": nsc(publish),
            },
        }
