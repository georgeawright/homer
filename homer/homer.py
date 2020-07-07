from homer.bubble_chamber import BubbleChamber
from homer.coderack import Coderack


class Homer:
    def __init__(self, bubble_chamber: BubbleChamber, coderack: Coderack):
        self.bubble_chamber = bubble_chamber
        self.coderack = coderack

    @classmethod
    def setup(cls):
        """Set up every component and sub-component from a configuration file"""
        pass

    def run(self):
        while self.bubble_chamber.result is None:
            self.coderack.select_and_run_codelet()
        return {
            "result": self.bubble_chamber.result,
            "satisfaction": self.bubble_chamber.satisfaction,
            "codelets_run": self.coderack.codelets_run,
        }
