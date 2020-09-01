import random

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Concept
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelets.evaluators import RawPerceptletLabelEvaluator
from homer.errors import MissingPerceptletError
from homer.workspace_location import WorkspaceLocation


class LabelEvaluationConcept(PerceptletType):
    def __init__(self, name: str = "label-evaluation"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(
        self, bubble_chamber: BubbleChamber
    ) -> RawPerceptletLabelEvaluator:
        if self.activation.as_scalar() > random.random():
            try:
                location = self.activation.get_high_location()
            except ValueError:
                return None
            try:
                perceptlet = bubble_chamber.workspace.raw_perceptlets.at(
                    location
                ).get_active()
                target_label = perceptlet.labels.get_active()
            except MissingPerceptletError:
                return None
            return RawPerceptletLabelEvaluator(
                bubble_chamber,
                self,
                bubble_chamber.concept_space.get_perceptlet_type_by_name("label"),
                target_label,
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
