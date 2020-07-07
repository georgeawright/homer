from typing import List

from homer.perceptlet import Perceptlet
from homer.trace import Trace
from homer.worldview import Worldview


class Workspace:
    def __init__(
        self, trace: Trace, worldview: Worldview, perceptlets: List[Perceptlet]
    ):
        self.trace = trace
        self.worldview = worldview
        self.perceptlets = perceptlets
