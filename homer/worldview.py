from typing import List

from homer.perceptlet import Perceptlet


class Worldview:
    def __init__(self, perceptlets: List[Perceptlet]):
        self.perceptlets = perceptlets
