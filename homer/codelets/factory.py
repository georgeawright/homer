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

    def _get_follow_up_type(self, action_type: Concept, structure_type: Concept):
        from homer.codelets.builders import (
            ChunkBuilder,
            CorrespondenceBuilder,
            LabelBuilder,
            RelationBuilder,
            WordBuilder,
            PhraseBuilder,
        )
        from homer.codelets.builders.view_builders import SimplexViewBuilder
        from homer.codelets.evaluators import (
            ChunkEvaluator,
            CorrespondenceEvaluator,
            LabelEvaluator,
            RelationEvaluator,
            WordEvaluator,
            PhraseEvaluator,
        )
        from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator
        from homer.codelets.selectors import (
            ChunkSelector,
            CorrespondenceSelector,
            LabelSelector,
            RelationSelector,
            WordSelector,
            PhraseSelector,
        )
        from homer.codelets.selectors.view_selectors import SimplexViewSelector

        return {
            "build": {
                # "chunk": ChunkBuilder,
                "label": LabelBuilder,
                # "relation": RelationBuilder,
                # "correspondence": CorrespondenceBuilder,
                # "view": SimplexViewBuilder,
                # "word": WordBuilder,
                "phrase": PhraseBuilder,
            },
            "evaluate": {
                # "chunk": ChunkEvaluator,
                "label": LabelEvaluator,
                # "relation": RelationEvaluator,
                # "correspondence": CorrespondenceEvaluator,
                # "view": SimplexViewEvaluator,
                # "word": WordEvaluator,
                "phrase": PhraseEvaluator,
            },
            "select": {
                # "chunk": ChunkSelector,
                "label": LabelSelector,
                # "relation": RelationSelector,
                # "correspondence": CorrespondenceSelector,
                # "view": SimplexViewSelector,
                # "word": WordSelector,
                "phrase": PhraseSelector,
            },
        }[action_type.name][structure_type.name]
