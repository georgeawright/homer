from homer import fuzzy
from .bubble_chamber import BubbleChamber
from .coderack import Coderack
from .errors import NoMoreCodelets
from .hyper_parameters import HyperParameters
from .logger import Logger
from .loggers import DjangoLogger
from .problem import Problem


class Homer:
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        coderack: Coderack,
        logger: Logger,
        activation_update_frequency: int = HyperParameters.ACTIVATION_UPDATE_FREQUENCY,
    ):
        self.bubble_chamber = bubble_chamber
        self.coderack = coderack
        self.logger = logger
        self.activation_update_frequency = activation_update_frequency

    def run(self):
        while self.bubble_chamber.result is None:
            # time.sleep(1)
            self.logger.log(self.coderack)
            if self.coderack.codelets_run % self.activation_update_frequency == 0:
                self.print_status_update()
                self.bubble_chamber.update_activations()
            try:
                self.coderack.select_and_run_codelet()
            except NoMoreCodelets:
                self.logger.log("no more codelets")
                self.print_results()
                break
            except Exception as e:
                raise e
        return {
            "result": self.bubble_chamber.result,
            "satisfaction": self.bubble_chamber.concept_space[
                "satisfaction"
            ].activation.as_scalar(),
            "codelets_run": self.coderack.codelets_run,
        }

    def print_status_update(self):
        codelets_run = self.coderack.codelets_run
        label_activation = (
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "label"
            ).activation.as_scalar()
        )
        group_activation = (
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "group"
            ).activation.as_scalar()
        )
        group_label_activation = (
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "group-label"
            ).activation.as_scalar()
        )
        correspondence_activation = (
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "correspondence"
            ).activation.as_scalar()
        )
        correspondence_label_activation = (
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "correspondence-label"
            ).activation.as_scalar()
        )
        textlet_activation = (
            self.bubble_chamber.concept_space.get_perceptlet_type_by_name(
                "textlet"
            ).activation.as_scalar()
        )
        print(
            "================================================================================"
        )
        print(
            f"codelets run: {codelets_run}; label: {label_activation}; group: {group_activation}; gr_label: {group_label_activation}; corresp: {correspondence_activation}; co_label: {correspondence_label_activation}; textlet: {textlet_activation}"
        )
        print(
            "================================================================================"
        )

    def print_results(self):
        for raw_perceptlet_field in self.bubble_chamber.workspace.input_sequence:
            for row in raw_perceptlet_field:
                for raw_perceptlet in row:
                    print(
                        ",".join(
                            [
                                label.parent_concept.name
                                for label in raw_perceptlet.labels
                            ]
                        ),
                        end="|",
                    )
                print("\n")
        for group in self.bubble_chamber.workspace.groups:
            print(
                f"{group.perceptlet_id} - location: {group.location}; size: {group.size}, activation: {group.activation.activation}"
            )
            print([(member.value, member.location) for member in group.members])
            print(
                "labels:",
                [(label.value, label.activation.activation) for label in group.labels],
            )
            print("textlets:", [textlet.value for textlet in group.textlets])
            print("\n")
        for correspondence in self.bubble_chamber.workspace.correspondences:
            print(
                f"{correspondence.perceptlet_id} from {correspondence.first_argument.perceptlet_id} to {correspondence.second_argument.perceptlet_id} in {correspondence.parent_concept.name}"
            )
            print(" ".join([label.value for label in correspondence.labels]))
            print("\n")
