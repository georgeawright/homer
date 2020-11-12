from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structures import Concept, Space
from homer.structures.links import Relation

from .chunk_builder import ChunkBuilder


class RelationBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_space: Space,
        target_structure_one: Structure,
        urgency: FloatBetweenOneAndZero,
        target_structure_two: Structure = None,
        parent_concept: Concept = None,
    ):
        Builder.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.target_space = target_space
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
        target_space: Space,
        target_structure_one: Structure,
        urgency: FloatBetweenOneAndZero,
        target_structure_two: Structure = None,
        parent_concept: Concept = None,
    ):
        qualifier = "TopDown" if parent_concept is not None else "BottomUp"
        codelet_id = ID.new(cls, qualifier)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_space,
            target_structure_one,
            urgency,
            target_structure_two,
            parent_concept,
        )

    def _passes_preliminary_checks(self):
        if self.target_structure_two is None:
            self.target_structure_two = self.target_space.contents.of_type(
                type(self.target_structure_one)
            ).get_exigent(exclude=[self.target_structure_one])
        if self.parent_concept is None:
            self.parent_concept = self.bubble_chamber.spaces[
                "relational concepts"
            ].contents.get_random()
        return not self.target_structure_one.has_relation(
            self.target_space, self.parent_concept, self.target_structure_two
        )

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classifier.classify(
            {
                "concept": self.parent_concept,
                "space": self.target_space,
                "start": self.target_structure_one,
                "end": self.target_structure_two,
            }
        )

    def _boost_activations(self):
        pass

    def _process_structure(self):
        relation = Relation(
            self.target_structure_one,
            self.target_structure_two,
            self.parent_concept,
            self.target_space,
            self.confidence,
        )
        self.target_space.contents.add(relation)
        self.target_structure_one.links_out.add(relation)
        self.target_structure_two.links_in.add(relation)
        self.bubble_chamber.relations.add(relation)
        self.child_structure = relation

    def _engender_follow_up(self):
        new_target = self.target_space.contents.get_unhappy()
        self.child_codelets.append(
            RelationBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_space,
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
                self.target_space,
                self.target_structure_one,
                self.target_structure_one.unhappiness,
            )
        )

    def _fail(self):
        new_target = self.target_space.contents.get_unhappy()
        self.child_codelets.append(
            ChunkBuilder.spawn(
                self.codelet_id, self.bubble_chamber, new_target, new_target.unhappiness
            )
        )
