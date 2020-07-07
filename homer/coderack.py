from homer.codelet import BubbleChamber
from homer.codelet import Codelet


class Coderack:
    def __init__(self, bubble_chamber: BubbleChamber):
        self.bubble_chamber = bubble_chamber
        self.codelets = []
        self.codelts_run = 0

    def select_and_run_codelet(self):
        self.calculate_randomness()
        codelet = self.select_codelet()
        follow_up = codelet.run()
        self.codelets_run += 1
        if follow_up is None:
            return
        if follow_up.target_perceptlet is None:
            new_target = self.bubble_chamber.select_target_perceptlet
            follow_up.target_perceptlet = new_target
        self.codelets.append(follow_up)

    def calculate_randomness(self):
        pass

    def select_codelet(self) -> Codelet:
        pass
