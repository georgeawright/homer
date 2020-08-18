import random

from homer.bubble_chamber import BubbleChamber
from homer.codelets.textlet_builder import TextletBuilder
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.errors import MissingPerceptletError
from homer.workspace_location import WorkspaceLocation


class TextletConcept(PerceptletType):
    def __init__(self, name: str = "textlet"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(self, bubble_chamber: BubbleChamber):
        activation = self.get_activation_as_scalar()
        if activation > random.random():
            try:
                target_perceptlet = bubble_chamber.workspace.groups.get_important()
            except MissingPerceptletError:
                return None
            if target_perceptlet is None:
                return None
            return TextletBuilder(
                bubble_chamber,
                self,
                target_perceptlet,
                target_perceptlet.exigency,
                self.concept_id,
            )

    def spawn_top_down_codelet(
        self,
        bubble_chamber: BubbleChamber,
        location: WorkspaceLocation,
        parent_concept: Concept,
    ):
        raise NotImplementedError
