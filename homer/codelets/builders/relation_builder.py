from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structures import Concept
from homer.structures.links import Relation

from .chunk_builder import ChunkBuilder


class RelationBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        structure_concept: Concept,
        bubble_chamber: BubbleChamber,
        target_structure_one: Structure,
        urgency: FloatBetweenOneAndZero,
        target_structure_two: Structure = None,
        parent_concept: Concept = None,
    ):
        Builder.__init__(self, codelet_id, parent_id, urgency)
        self.structure_concept = structure_concept
        self.bubble_chamber = bubble_chamber
        self.target_structure_one = target_structure_one
        self.target_structure_two = target_structure_two
        self.parent_concept = parent_concept
        self.confidence = 0.0
        self.child_structure = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structure_one: Structure,
        urgency: FloatBetweenOneAndZero,
        target_structure_two: Structure = None,
        parent_concept: Concept = None,
    ):
        codelet_id = ""
        structure_concept = bubble_chamber.concepts["relation"]
        return cls(
            codelet_id,
            parent_id,
            structure_concept,
            bubble_chamber,
            target_structure_one,
            urgency,
            target_structure_two,
            parent_concept,
        )

    def _passes_preliminary_checks(self):
        if self.target_structure_two is None:
            # parent concept and space need to be compatible
            self.target_structure_two = (
                self.target_structure_one.parent_spaces.get_random().contents.get_exigent()
            )
        if self.parent_concept is None:
            # parent concept and space need to be compatible
            self.parent_concept = self.bubble_chamber.get_random_relation_concept()
        return not self.target_structure_one.has_relation(
            self.parent_concept, self.target_structure_two
        )

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classify(
            self.target_structure_one, self.target_structure_two
        )

    def _boost_activations(self):
        pass

    def _process_structure(self):
        relation = Relation(
            self.target_structure_one, self.target_structure_two, self.parent_concept
        )
        self.target_structure_one.add_relation(relation)
        self.target_structure_two.add_relation(relation)
        self.bubble_chamber.add_relation(relation)
        self.child_structure = relation

    def _engender_follow_up(self):
        new_target = self.target_structure_one.nearby.get_unhappy()
        self.child_codelets.append(
            RelationBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                new_target,
                self.confidence,
                self.parent_concept,
            )
        )

    def _fizzle(self):
        self.child_codelets.append(
            RelationBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_structure_one,
                self.target_structure_one.unhappiness,
            )
        )

    def _fail(self):
        new_target = self.target_structure_one.parent_space.contents.get_random()
        self.child_codelets.append(
            ChunkBuilder.spawn(
                self.codelet_id, self.bubble_chamber, new_target, new_target.unhappiness
            )
        )
