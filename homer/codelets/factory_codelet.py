import random

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
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
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Concept


class FactoryCodelet(Codelet):
    """Spawns a new codelet according to concept activations in the bubble chamber."""

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
        action_type = self.bubble_chamber.spaces["activities"].contents.get_random()
        links_to_structure_nodes = StructureCollection(
            {
                link
                for link in action_type.links_out
                if link.end in self.bubble_chamber.spaces["structures"].contents
            }
        )
        structure_type = links_to_structure_nodes.get_random().end
        follow_up_type = self._get_follow_up_type(action_type, structure_type)
        proportion_of_follow_up_type_on_coderack = (
            self.coderack.number_of_codelets_of_type(follow_up_type) / 50
        )
        if proportion_of_follow_up_type_on_coderack < random.random():
            follow_up = follow_up_type.make(self.codelet_id, self.bubble_chamber)
            self.child_codelets.append(follow_up)

    def _get_follow_up_type(self, action_type: Concept, structure_type: Concept):
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
