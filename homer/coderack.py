import random

from homer.codelet import BubbleChamber
from homer.codelet import Codelet


class Coderack:
    def __init__(self, bubble_chamber: BubbleChamber):
        self.bubble_chamber = bubble_chamber
        self.codelets = []
        self.codelets_run = 0

    def select_and_run_codelet(self):
        self.calculate_randomness()
        codelet = self.select_codelet()
        follow_up = codelet.run()
        self.codelets_run += 1
        if follow_up is not None:
            self.codelets.append(follow_up)

    def calculate_randomness(self) -> float:
        return (1 - self.bubble_chamber.satisfaction) * random.random()

    def select_codelet(self) -> Codelet:
        pass
