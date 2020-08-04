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
            if self.coderack.codelets_run % self.activation_update_frequency == 0:
                self.print_status_update()
                self.bubble_chamber.update_activations()
                self.coderack.get_more_codelets()
            self.coderack.select_and_run_codelet()
        return {
            "result": self.bubble_chamber.result,
            "satisfaction": self.bubble_chamber.satisfaction,
            "codelets_run": self.coderack.codelets_run,
        }

    def print_status_update(self):
        codelets_run = self.coderack.codelets_run
        label_activation = self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
            "label"
        ).activation_pattern.activation
        group_activation = self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
            "group"
        ).activation_pattern.activation
        group_label_activation = self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
            "group-label"
        ).activation_pattern.activation
        correspondence_activation = self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
            "correspondence"
        ).activation_pattern.activation
        correspondence_label_activation = self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
            "correspondence-label"
        ).activation_pattern.activation
        print(
            "================================================================================"
        )
        print(
            f"codelets run: {codelets_run}; label: {label_activation}; group: {group_activation}; gr_label: {group_label_activation}; corresp: {correspondence_activation}; co_label: {correspondence_label_activation}"
        )
        print(
            "================================================================================"
        )
