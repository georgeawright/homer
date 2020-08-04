import random

from homer.codelet import BubbleChamber
from homer.codelet import Codelet
from homer.errors import NoMoreCodelets


class Coderack:
    def __init__(self, bubble_chamber: BubbleChamber):
        self.bubble_chamber = bubble_chamber
        self.codelets = []
        self.codelets_run = 0

    def select_and_run_codelet(self):
        codelet = self.select_codelet()
        follow_up = codelet.run()
        self.codelets_run += 1
        if follow_up is not None:
            self.codelets.append(follow_up)

    def select_codelet(self) -> Codelet:
        if len(self.codelets) < 1:
            self.get_more_codelets()
        codelet_choice = None
        highest_weight = 0
        for codelet in self.codelets:
            weight = codelet.urgency + random.random() * self._randomness()
            if weight > highest_weight:
                highest_weight = weight
                codelet_choice = codelet
        if codelet_choice is None:
            print("No more codelets")
            exit()
        self.codelets.remove(codelet_choice)
        return codelet_choice

    def get_more_codelets(self):
        for concept in self.bubble_chamber.concept_space.perceptlet_types:
            codelet = concept.spawn_codelet(self.bubble_chamber)
            if codelet is not None:
                self.codelets.append(codelet)

    def _randomness(self) -> float:
        return 1 - self.bubble_chamber.satisfaction
