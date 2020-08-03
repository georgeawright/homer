import random

from homer.bubble_chamber import BubbleChamber
from homer.codelets.group_builder import GroupBuilder
from homer.concepts.perceptlet_concept import PerceptletConcept


class GroupConcept(PerceptletConcept):
    def __init__(self, name: str = "group"):
        PerceptletConcept.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber):
        activation = self.get_activation_as_scalar()
        if activation > random.random():
            target_perceptlet = bubble_chamber.get_raw_perceptlet()
            return GroupBuilder(
                bubble_chamber, self, target_perceptlet, target_perceptlet.exigency
            )
