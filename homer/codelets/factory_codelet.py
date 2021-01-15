import random

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.codelets.builders import (
    ChunkBuilder,
    CorrespondenceBuilder,
    LabelBuilder,
    RelationBuilder,
    ViewBuilder,
    WordBuilder,
)
from homer.codelets.evaluators import (
    ChunkEvaluator,
    CorrespondenceEvaluator,
    LabelEvaluator,
    RelationEvaluator,
    ViewEvaluator,
)
from homer.codelets.selectors import (
    ChunkSelector,
    CorrespondenceSelector,
    LabelSelector,
    RelationSelector,
    ViewSelector,
)
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Concept


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
        try:
            return {
                "build": {
                    "chunk": ChunkBuilder,
                    "label": LabelBuilder,
                    "relation": RelationBuilder,
                    "correspondence": CorrespondenceBuilder,
                    "view": ViewBuilder,
                },
                "evaluate": {
                    "chunk": ChunkEvaluator,
                    "label": LabelEvaluator,
                    "relation": RelationEvaluator,
                    "correspondence": CorrespondenceEvaluator,
                    "view": ViewEvaluator,
                },
                "select": {
                    "chunk": ChunkSelector,
                    "label": LabelSelector,
                    "relation": RelationSelector,
                    "correspondence": CorrespondenceSelector,
                    "view": ViewSelector,
                },
            }[action_type.name][structure_type.name]
        except KeyError:
            # this should be removed when all codelet types have been added to the dict
            raise MissingStructureError
