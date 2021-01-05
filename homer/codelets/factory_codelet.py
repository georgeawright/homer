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
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, urgency)

    def run(self) -> CodeletResult:
        try:
            self._engender_follow_up()
        except MissingStructureError:
            return self.run()
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                1 - self.bubble_chamber.satisfaction,
            )
        )
        self.result = CodeletResult.SUCCESS
        return self.result

    def _engender_follow_up(self):
        action_type = self.bubble_chamber.spaces["activities"].contents.get_active()
        links_to_structure_nodes = StructureCollection(
            {
                link
                for link in action_type.links_out
                if link.end in self.bubble_chamber.spaces["structures"].contents
            }
        )
        structure_type = links_to_structure_nodes.get_active().end
        follow_up_type = self._get_follow_up_type(action_type, structure_type)
        follow_up = follow_up_type.make(self.codelet_id, self.bubble_chamber)
        self.child_codelets.append(follow_up)

    def _get_follow_up_type(self, action_type: Concept, structure_type: Concept):
        print(action_type.name)
        print(structure_type.name)
        try:
            return {
                "build": {
                    "chunk": ChunkBuilder,
                    "label": LabelBuilder,
                    "relation": RelationBuilder,
                },
                "evaluate": {
                    "chunk": ChunkEvaluator,
                    "label": LabelEvaluator,
                    "relation": RelationEvaluator,
                },
                "select": {
                    "chunk": ChunkSelector,
                    "label": LabelSelector,
                    "relation": RelationSelector,
                },
            }[action_type.name][structure_type.name]
        except KeyError:
            # this should be removed when all codelet types have been added to the dict
            raise MissingStructureError
