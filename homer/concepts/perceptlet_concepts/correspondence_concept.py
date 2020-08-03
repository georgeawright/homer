import random
import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.correspondence_suggester import CorrespondenceSuggester
from homer.concepts.perceptlet_concept import PerceptletConcept


class CorrespondenceConcept(PerceptletConcept):
    def __init__(self, name: str = "correspondence"):
        PerceptletConcept.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber):
        activation = self.get_activation_as_scalar()
        if activation > random.random():
            target_groups = bubble_chamber.get_random_groups(2)
            urgency = statistics.fmean((group.exigency for group in target_groups))
            return CorrespondenceSuggester(bubble_chamber, *target_groups, urgency)
