from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Factory
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collection_keys import activation
from linguoplotter.structure_collections import StructureSet
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
        targets,
        urgency: FloatBetweenOneAndZero,
    ):
        Factory.__init__(
            self, codelet_id, parent_id, bubble_chamber, coderack, targets, urgency
        )

    @property
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
        self._get_parent_concept()
        follow_up_class = self._get_follow_up_class()
        rand = self.bubble_chamber.random_machine.generate_number()
        if self.coderack.proportion_of_codelets_of_type(follow_up_class) < rand:
            follow_up = follow_up_class.make_top_down(
                self.codelet_id, self.bubble_chamber, self.targets["concept"]
            )
            self.child_codelets.append(follow_up)

    def _get_parent_concept(self) -> Concept:
        self.targets["concept"] = (
            StructureSet.union(
                self._get_label_concepts(),
                self._get_relational_concepts(),
            )
            .filter(lambda x: x.is_fully_active())
            .get()
        )

    def _get_follow_up_class(self):
        action_concept = self.bubble_chamber.concepts["suggest"]
        if (
            self.targets["concept"].structure_type == Label
            and self.targets["concept"].parent_space.structure_type == Label
        ):
            space_concept = self.bubble_chamber.concepts["inner"]
        elif (
            self.targets["concept"].structure_type == Label
            and self.targets["concept"].parent_space.structure_type == Relation
        ):
            space_concept = self.bubble_chamber.concepts["outer"]
        else:
            space_concept = self.bubble_chamber.random_machine.select(
                [
                    self.bubble_chamber.concepts["inner"],
                    self.bubble_chamber.concepts["outer"],
                ],
                key=activation,
            )
        direction_concept = self.bubble_chamber.concepts["forward"]
        if self.targets["concept"] in self._get_label_concepts():
            structure_concept = self.bubble_chamber.concepts["label"]
        if self.targets["concept"] in self._get_relational_concepts():
            structure_concept = self.bubble_chamber.concepts["relation"]
        return self._get_codelet_type_from_concepts(
            action=action_concept,
            space=space_concept,
            direction=direction_concept,
            structure=structure_concept,
        )

    def _get_label_concepts(self) -> StructureSet:
        return self.bubble_chamber.concepts.where(structure_type=Label).where_not(
            classifier=None
        )

    def _get_relational_concepts(self) -> StructureSet:
        return self.bubble_chamber.concepts.where(structure_type=Relation).where_not(
            classifier=None
        )
