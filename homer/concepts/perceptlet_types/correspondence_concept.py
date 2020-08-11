import random
import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.correspondence_suggester import CorrespondenceSuggester
from homer.concepts.perceptlet_type import PerceptletType
from homer.errors import MissingPerceptletError


class CorrespondenceConcept(PerceptletType):
    def __init__(self, name: str = "correspondence"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber):
        activation = self.get_activation_as_scalar()
        randomness = random.random()
        if activation > randomness:
            try:
                target_groups = bubble_chamber.get_random_groups(2)
            except MissingPerceptletError:
                return None
            urgency = statistics.fmean((group.exigency for group in target_groups))
            return CorrespondenceSuggester(
                bubble_chamber, self, *target_groups, urgency, self.concept_id,
            )
