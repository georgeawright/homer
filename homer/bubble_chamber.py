from homer.concept_space import ConceptSpace
from homer.event_trace import EventTrace
from homer.perceptlet import Perceptlet
from homer.workspace import Workspace
from homer.worldview import Worldview


class BubbleChamber:
    def __init__(
        self,
        concept_space: ConceptSpace,
        event_trace: EventTrace,
        workspace: Workspace,
        worldview: Worldview,
    ):
        self.concept_space = concept_space
        self.event_trace = event_trace
        self.workspace = workspace
        self.worldview = worldview
        self.result = None

    @property
    def satisfaction(self) -> float:
        """Calculate and return overall satisfaction with perceptual structures"""
        pass

    def select_target_perceptlet(self) -> Perceptlet:
        """Return a target for a codelet"""
        pass
