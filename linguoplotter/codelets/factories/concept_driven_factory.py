from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Factory
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structure_collection_keys import activation
from linguoplotter.structures.links import Label, Relation
from linguoplotter.structures.nodes import Concept


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

    def follow_up_urgency(self):
        if self.bubble_chamber.focus.view is None:
            try:
                return max(
                    min(
                        [
                            self.bubble_chamber.satisfaction,
                            self.child_codelets[0].urgency,
                        ]
                    ),
                    self.coderack.MINIMUM_CODELET_URGENCY,
                )
            except IndexError:
                return max(
                    self.bubble_chamber.satisfaction,
                    self.coderack.MINIMUM_CODELET_URGENCY,
                )
        return self.coderack.MINIMUM_CODELET_URGENCY

    def _engender_follow_up(self):
        parent_concept = self._get_parent_concept()
        follow_up_class = self._get_follow_up_class(parent_concept)
        rand = self.bubble_chamber.random_machine.generate_number()
        if self.coderack.proportion_of_codelets_of_type(follow_up_class) < rand:
            follow_up = follow_up_class.make_top_down(
                self.codelet_id, self.bubble_chamber, parent_concept
            )
            self.child_codelets.append(follow_up)

    def _get_parent_concept(self) -> Concept:
        return StructureCollection.union(
            self._get_label_concepts(),
            self._get_relational_concepts(),
        ).get(key=activation)

    def _get_follow_up_class(self, parent_concept: Concept):
        action_concept = self.bubble_chamber.concepts["suggest"]
        space_concept = self.bubble_chamber.concepts["inner"]
        direction_concept = self.bubble_chamber.concepts["forward"]
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

    def _get_label_concepts(self) -> StructureCollection:
        return self.bubble_chamber.concepts.where(structure_type=Label).where_not(
            classifier=None
        )

    def _get_relational_concepts(self) -> StructureCollection:
        return self.bubble_chamber.concepts.where(structure_type=Relation).where_not(
            classifier=None
        )
