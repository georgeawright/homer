import random

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Factory
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation
from homer.structures.nodes import Concept
from homer.structures.spaces import ConceptualSpace


class ConceptDrivenFactory(Factory):
    """Finds an active concept to spawn a top down codelet for"""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        Factory.__init__(self, codelet_id, parent_id, bubble_chamber, coderack, urgency)

    def _engender_follow_up(self):
        parent_concept = self._get_parent_concept()
        follow_up_class = self._get_follow_up_class(parent_concept)
        rand = random.random()
        if self.coderack.proportion_of_codelets_of_type(follow_up_class) < rand:
            follow_up = follow_up_class.make_top_down(
                self.codelet_id, self.bubble_chamber, parent_concept
            )
            self.child_codelets.append(follow_up)

    def _get_parent_concept(self) -> Concept:
        return StructureCollection.union(
            # self.bubble_chamber.rules,
            self._get_correspondential_concepts(),
            self._get_label_concepts(),
            self._get_relational_concepts(),
        ).get(key=activation)

    def _get_follow_up_class(self, parent_concept: Concept):
        action_concept = self.bubble_chamber.concepts["suggest"]
        space_concept = self.bubble_chamber.concepts["inner"]
        direction_concept = self.bubble_chamber.concepts["forward"]
        if parent_concept in self.bubble_chamber.rules:
            structure_concept = self.bubble_chamber.concepts["phrase"]
        if parent_concept in self._get_correspondential_concepts():
            structure_concept = self.bubble_chamber.concepts["correspondence"]
        if parent_concept in self._get_label_concepts():
            structure_concept = self.bubble_chamber.concepts["label"]
        if parent_concept in self._get_relational_concepts():
            structure_concept = self.bubble_chamber.concepts["relation"]
        return self._get_codelet_type_from_concepts(
            action=action_concept,
            space=space_concept,
            direction=direction_concept,
            structure=structure_concept,
        )

    def _get_correspondential_concepts(self) -> StructureCollection:
        return StructureCollection(
            {
                concept
                for conceptual_space in self.bubble_chamber.spaces[
                    "correspondential concepts"
                ].contents.of_type(ConceptualSpace)
                for concept in conceptual_space.contents.of_type(Concept)
            }
        ).where_not(classifier=None)

    def _get_label_concepts(self) -> StructureCollection:
        return StructureCollection(
            {
                concept
                for conceptual_space in self.bubble_chamber.spaces[
                    "label concepts"
                ].contents.of_type(ConceptualSpace)
                for concept in conceptual_space.contents.of_type(Concept)
            }
        ).where_not(classifier=None)

    def _get_relational_concepts(self) -> StructureCollection:
        return StructureCollection(
            {
                concept
                for conceptual_space in self.bubble_chamber.spaces[
                    "relational concepts"
                ].contents.of_type(ConceptualSpace)
                for concept in conceptual_space.contents.of_type(Concept)
            }
        ).where_not(classifier=None)
