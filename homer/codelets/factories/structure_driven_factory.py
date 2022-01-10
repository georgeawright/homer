from homer.bubble_chamber import BubbleChamber
from homer.codelets import Factory
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structure_collection_keys import unhappiness


class StructureDrivenFactory(Factory):
    """Finds an unhappy structure to do work on"""

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
        structure = input_space.contents.get(key=unhappiness)
        follow_up_class = self._get_follow_up_class(structure)
        rand = self.bubble_chamber.random_machine.generate_random_number()
        if self.coderack.proportion_of_codelets_of_type(follow_up_class) < rand:
            follow_up = follow_up_class.make(self.codelet_id, self.bubble_chamber)
            self.child_codelets.append(follow_up)

    def _get_follow_up_class(self, structure: Structure):
        action_concept = self.bubble_chamber.concepts["suggest"]
        space_concept = self.bubble_chamber.concepts["inner"]
        direction_concept = self.bubble_chamber.concepts["forward"]

        lowest_unhappiness = structure.unlabeledness
        structure_concept = self.bubble_chamber["label"]
        if structure.unrelatedness < lowest_unhappiness:
            lowest_unhappiness = structure.unrelatedness
            structure_concept = self.bubble_chamber["relation"]
        if structure.uncorrespondedness < lowest_unhappiness:
            lowest_unhappiness = structure.uncorrespondedness
            structure_concept = self.bubble_chamber["correspondence"]
        if structure.is_chunk and structure.unchunkedness < lowest_unhappiness:
            structure_concept = self.bubble_chamber["chunk"]
        return self._get_codelet_type_from_concepts(
            action=action_concept,
            space=space_concept,
            direction=direction_concept,
            structure=structure_concept,
        )
