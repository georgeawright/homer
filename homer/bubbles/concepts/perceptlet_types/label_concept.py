from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concept import Concept
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelets import BottomUpRawPerceptletLabeler, RawPerceptletLabeler
from homer.workspace_location import WorkspaceLocation


class LabelConcept(PerceptletType):
    def __init__(self, name: str = "label"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(
        self, bubble_chamber: BubbleChamber
    ) -> Optional[BottomUpRawPerceptletLabeler]:
        if self.activation.is_high():
            target_perceptlet = bubble_chamber.workspace.raw_perceptlets.get_unhappy()
            return BottomUpRawPerceptletLabeler(
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
        target_perceptlet = bubble_chamber.workspace.raw_perceptlets.at(
            location
        ).get_unhappy()
        return RawPerceptletLabeler(
            bubble_chamber,
            self,
            parent_concept,
            target_perceptlet,
            target_perceptlet.exigency,
            parent_concept.concept_id,
        )
