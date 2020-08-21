from typing import Set

from .bubbles.perceptlet import Perceptlet


class Worldview:
    def __init__(self, perceptlets: Set[Perceptlet]):
        self.perceptlets = perceptlets

    def add_perceptlet(self, perceptlet: Perceptlet):
        self.perceptlets.add(perceptlet)

    def remove_perceptlet(self, perceptlet: Perceptlet):
        self.perceptlets.remove(perceptlet)
