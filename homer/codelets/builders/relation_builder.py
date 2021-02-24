from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.links import Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import ConceptualSpace

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
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_space = target_space
        self.target_structure_one = target_structure_one
        self.target_structure_two = target_structure_two
        self.parent_concept = parent_concept
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
            target_structure_two=target_structure_two,
            parent_concept=parent_concept,
        )

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target_space = bubble_chamber.working_spaces.where(
            no_of_dimensions=1
        ).get_random()
        target = target_space.contents.of_type(Chunk).get_exigent()
        return cls.spawn(
            parent_id, bubble_chamber, target_space, target, target.exigency
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        if self.target_structure_two is None:
            try:
                self.target_structure_two = self.target_space.contents.of_type(
                    type(self.target_structure_one)
                ).get_exigent(exclude=[self.target_structure_one])
            except MissingStructureError:
                return False
        if self.parent_concept is None:
            try:
                relational_conceptual_spaces = self.bubble_chamber.spaces[
                    "relational concepts"
                ].contents.of_type(ConceptualSpace)
                compatible_conceptual_spaces = StructureCollection(
                    {
                        space
                        for space in relational_conceptual_spaces
                        if space.is_compatible_with(self.target_space)
                    }
                )
                self.parent_concept = (
                    compatible_conceptual_spaces.get_random()
                    .contents.of_type(Concept)
                    .get_random()
                )
            except MissingStructureError:
                return False
        return not self.target_structure_one.has_relation(
            self.target_space,
            self.parent_concept,
            self.target_structure_one,
            self.target_structure_two,
        )

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classifier.classify(
            concept=self.parent_concept,
            space=self.target_space,
            start=self.target_structure_one,
            end=self.target_structure_two,
        )

    def _process_structure(self):
        relation = Relation(
            ID.new(Relation),
            self.codelet_id,
            self.target_structure_one,
            self.target_structure_two,
            self.parent_concept,
            self.target_space,
            0,
        )
        relation.activation = self.INITIAL_STRUCTURE_ACTIVATION
        self.target_space.add(relation)
        self.target_structure_one.links_out.add(relation)
        self.target_structure_two.links_in.add(relation)
        self.bubble_chamber.relations.add(relation)
        self.child_structure = relation
        self.bubble_chamber.logger.log(relation)

    def _engender_follow_up(self):
        from homer.codelets.evaluators import RelationEvaluator

        self.child_codelets.append(
            RelationEvaluator.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.child_structure,
                self.confidence,
            )
        )

    def _fizzle(self):
        self.child_codelets.append(
            RelationBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_space,
                self.target_structure_one,
                self.urgency / 2,
            )
        )

    def _fail(self):
        new_target = self.target_space.contents.of_type(Chunk).get_unhappy()
        self.child_codelets.append(
            ChunkBuilder.spawn(
                self.codelet_id, self.bubble_chamber, new_target, new_target.unhappiness
            )
        )
