from .bubble_chamber import BubbleChamber
from .coderack import Coderack
from .errors import NoMoreCodelets
from .hyper_parameters import HyperParameters
from .logger import Logger
from .structure_collection import StructureCollection
from .structures.spaces import ConceptualSpace


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

    @classmethod
    def setup(cls, logger: Logger):
        top_level_conceptual_space = ConceptualSpace(
            "top_level_space",
            "",
            "top level",
            None,
            [None],
            StructureCollection(),
            0,
            [],
            [],
        )
        logger.log(top_level_conceptual_space)
        top_level_working_space = top_level_conceptual_space.instance_in_space(
            None, name="top level working"
        )
        logger.log(top_level_working_space)
        bubble_chamber = BubbleChamber.setup(logger)
        bubble_chamber.conceptual_spaces.add(top_level_conceptual_space)
        bubble_chamber.working_spaces.add(top_level_working_space)
        coderack = Coderack.setup(bubble_chamber, logger)
        return cls(bubble_chamber, coderack, logger)

    def run(self):
        while self.bubble_chamber.result is None:
            try:
                self.logger.log(self.coderack)
                if self.coderack.codelets_run % self.activation_update_frequency == 0:
                    self.print_status_update()
                    self.bubble_chamber.spread_activations()
                    self.bubble_chamber.update_activations()
                if self.coderack.codelets_run >= 30000:
                    raise NoMoreCodelets
                self.coderack.select_and_run_codelet()
            except NoMoreCodelets:
                self.logger.log("no more codelets")
                self.print_results()
                break
            except Exception as e:
                raise e
        self.logger.log(self.coderack)
        self.print_results()
        return {
            "result": self.bubble_chamber.result,
            "satisfaction": self.bubble_chamber.satisfaction,
            "codelets_run": self.coderack.codelets_run,
        }

    def print_status_update(self):
        codelets_run = self.coderack.codelets_run
        bubble_chamber_satisfaction = self.bubble_chamber.satisfaction
        build_activation = self.bubble_chamber.concepts["build"].activation
        evaluate_activation = self.bubble_chamber.concepts["evaluate"].activation
        select_activation = self.bubble_chamber.concepts["select"].activation
        print(
            "================================================================================"
        )
        print(
            f"codelets run: {codelets_run}; "
            + f"satisfaction: {bubble_chamber_satisfaction}; "
            + f"build: {build_activation}; "
            + f"evaluate: {evaluate_activation}; "
            + f"select: {select_activation}; "
        )
        print(
            "================================================================================"
        )

    def print_results(self):
        print(f"codelets run: {self.coderack.codelets_run}")
        print(f"satisfaction: {self.bubble_chamber.satisfaction}")
        print(f"result: {self.bubble_chamber.result}")
