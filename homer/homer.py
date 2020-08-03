from homer.bubble_chamber import BubbleChamber
from homer.coderack import Coderack
from homer.hyper_parameters import HyperParameters


class Homer:
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        coderack: Coderack,
        activation_update_frequency: int = HyperParameters.ACTIVATION_UPDATE_FREQUENCY,
    ):
        self.bubble_chamber = bubble_chamber
        self.coderack = coderack
        self.activation_update_frequency = activation_update_frequency

    @classmethod
    def setup(cls):
        """Set up every component and sub-component from a configuration file"""
        # include
        # codelet classifier weights
        # concepts, including depths, prototypes, distance metrics
        # workspace with raw perceptlets

    def run(self):
        while self.bubble_chamber.result is None:
            print(self.coderack.codelets)
            if self.coderack.codelets_run % self.activation_update_frequency == 0:
                self.bubble_chamber.update_activations()
                self.coderack.get_more_codelets()
            self.coderack.select_and_run_codelet()
        return {
            "result": self.bubble_chamber.result,
            "satisfaction": self.bubble_chamber.satisfaction,
            "codelets_run": self.coderack.codelets_run,
        }
