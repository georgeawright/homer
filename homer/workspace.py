from typing import List

from homer.perceptlet import Perceptlet
from homer.event_trace import EventTrace
from homer.worldview import Worldview


class Workspace:
    def __init__(
        self,
        event_trace: EventTrace,
        worldview: Worldview,
        perceptlets: List[Perceptlet],
    ):
        self.event_trace = event_trace
        self.worldview = worldview
        self.perceptlets = perceptlets
