from typing import List

from .bubbles.perceptlet import Perceptlet


class EventTrace:
    def __init__(self, perceptlets: List[Perceptlet]):
        self.perceptlets = perceptlets
