import random

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Concept
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelets.selectors import CorrespondenceSelector
from homer.errors import MissingPerceptletError
from homer.workspace_location import WorkspaceLocation


class CorrespondenceSelectionConcept(PerceptletType):
    def __init__(self, name: str = "correspondence-selection"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber) -> CorrespondenceSelector:
        if self.activation.as_scalar() > random.random():
            try:
                location = self.activation.get_high_location()
            except ValueError:
                return None
            try:
                champion = bubble_chamber.workspace.correspondences.at(
                    location
                ).get_most_active()
            except MissingPerceptletError:
                return None
            return CorrespondenceSelector(
                bubble_chamber,
                self,
                bubble_chamber.concept_space.get_perceptlet_type_by_name(
                    "correspondence"
                ),
                champion,
                self.activation.at(location),
                self.concept_id,
            )

    def spawn_top_down_codelet(
        self,
        bubble_chamber: BubbleChamber,
        location: WorkspaceLocation,
        parent_concept: Concept,
    ):
        raise NotImplementedError
