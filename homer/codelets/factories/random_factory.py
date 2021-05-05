import random

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Factory
from homer.float_between_one_and_zero import FloatBetweenOneAndZero


class RandomFactory(Factory):
    """Spawns a random new codelet and a copy of itself"""

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
        follow_up_class = self._decide_follow_up_class()
        proportion_of_follow_up_class_on_coderack = (
            self.coderack.number_of_codelets_of_type(follow_up_class) / 50
        )  # TODO this should be divided by umber of codelets on coderack
        if proportion_of_follow_up_class_on_coderack < random.random():
            follow_up = follow_up_class.make(self.codelet_id, self.bubble_chamber)
            self.child_codelets.append(follow_up)

    def _decide_follow_up_class(self):
        follow_up_theme = random.sample(list(self.codelet_themes().values()), 1)[0]
        return self._get_codelet_type_from_concepts(
            action=follow_up_theme["actions"].get_random(),
            space=follow_up_theme["spaces"].get_random(),
            direction=follow_up_theme["directions"].get_random(),
            structure=follow_up_theme["structures"].get_random(),
        )
