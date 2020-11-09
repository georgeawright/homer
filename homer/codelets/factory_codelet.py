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
        action_type = self.bubble_chamber.concepts["actions"].get_active()
        structure_type = self.bubble_chamber.concepts["structures"].get_active()
        self._engender_follow_up(action_type, structure_type)
        self.child_codelets.append(
            self.spawn(
                self.codelet_id, self.bubble_chamber, self.bubble_chamber.satisfaction
            )
        )
        self.result = CodeletResult.SUCCESS
        return self.result

    def _engender_follow_up(self, action_type: Concept, structure_type: Concept):
        if action_type == self.bubble_chamber.concepts["builder"]:
            if structure_type == self.bubble_chamber.concepts["chunk"]:
                target = self.bubble_chamber.chunks.get_unhappy()
                follow_up = ChunkBuilder.spawn(
                    self.codelet_id, self.bubble_chamber, target, target.unhappiness
                )
            elif structure_type == self.bubble_chamber.concepts["correspondence"]:
                target_space = self.bubble_chamber.spaces.get_active()
                target = StructureCollection.union(
                    target_space.chunks,
                    target_space.labels,
                    target_space.relations,
                ).get_unhappy()
                follow_up = CorrespondenceBuilder.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target_space,
                    target,
                    target.unhappiness,
                )
            elif structure_type == self.bubble_chamber.concepts["label"]:
                target = self.bubble_chamber.chunks.get_unhappy()
                follow_up = LabelBuilder.spawn(
                    self.codelet_id, self.bubble_chamber, target, target.unhappiness
                )
            elif structure_type == self.bubble_chamber.concepts["relation"]:
                target = StructureCollection.union(
                    self.bubble_chamber.chunks,
                    self.bubble_chamber.relations,
                ).get_unhappy()
                target_space = target.parent_spaces.get_random()
                follow_up = RelationBuilder.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target_space,
                    target,
                    target.unhappiness,
                )
            elif structure_type == self.bubble_chamber.concepts["view"]:
                target = self.bubble_chamber.correspondences.get_unhappy()
                follow_up = ViewBuilder.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target,
                    target.unhappiness,
                )
            elif structure_type == self.bubble_chamber.concepts["word"]:
                target_view = self.bubble_chamber.view.get_unhappy()
                target_correspondence = (
                    self.bubble_chamber.correspondences.get_unhappy()
                )
                follow_up = WordBuilder.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target_view,
                    target_correspondence,
                    target_correspondence.unhappiness,
                )
        elif action_type == self.bubble_chamber.concepts["evaluator"]:
            pass
        elif action_type == self.bubble_chamber.concepts["selector"]:
            pass
        self.child_codelets.append(follow_up)
