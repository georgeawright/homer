from homer.bubble_chamber import BubbleChamber
from homer.codelets import Factory
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection_keys import activation


class RationalFactory(Factory):
    """Spawns a new codelet according to concept activations and a copy of itself"""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        Factory.__init__(self, codelet_id, parent_id, bubble_chamber, coderack, urgency)

    def follow_up_satisfaction(self) -> FloatBetweenOneAndZero:
        return self.bubble_chamber.satisfaction

    def _engender_follow_up(self):
        follow_up_class = self._decide_follow_up_class()
        rand = self.bubble_chamber.random_machine.generate_number()
        if self.coderack.proportion_of_codelets_of_type(follow_up_class) < rand:
            follow_up = follow_up_class.make(self.codelet_id, self.bubble_chamber)
            self.child_codelets.append(follow_up)

    def _decide_follow_up_class(self):
        follow_up_theme = self.bubble_chamber.random_machine.select(
            self.codelet_themes().values()
        )
        return self._get_codelet_type_from_concepts(
            action=follow_up_theme["actions"].get(key=activation),
            space=follow_up_theme["spaces"].get(key=activation),
            direction=follow_up_theme["directions"].get(key=activation),
            structure=follow_up_theme["structures"].get(key=activation),
        )
