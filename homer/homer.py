from typing import Dict

from .bubble_chamber import BubbleChamber
from .coderack import Coderack
from .errors import NoMoreCodelets
from .hyper_parameters import HyperParameters
from .interpreter import Interpreter
from .logger import Logger
from .structure_collection import StructureCollection
from .structures.spaces import ConceptualSpace


class Homer:
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        coderack: Coderack,
        interpreter: Interpreter,
        loggers: Dict[str, Logger],
        activation_update_frequency: int = HyperParameters.ACTIVATION_UPDATE_FREQUENCY,
    ):
        self.bubble_chamber = bubble_chamber
        self.coderack = coderack
        self.interpreter = interpreter
        self.loggers = loggers
        self.activation_update_frequency = activation_update_frequency

    @classmethod
    def setup(cls, loggers: Dict[str, Logger], random_seed: int = None):
        bubble_chamber = BubbleChamber.setup(loggers, random_seed=random_seed)
        coderack = Coderack.setup(bubble_chamber, loggers)
        interpreter = Interpreter(bubble_chamber)
        return cls(bubble_chamber, coderack, interpreter, loggers)

    def run_program(self, program: str):
        # possibly first interpret / sort out internal stuff
        # that might be done in bubble chamber setup
        self.interpreter.interpret_string(program)
        self.run()

    def reset(self):
        self.logger.reset()
        self.bubble_chamber = BubbleChamber.setup(self.logger)
        self.coderack = Coderack.setup(self.bubble_chamber, self.logger)

    def run(self):
        while self.bubble_chamber.result is None:
            try:
                if self.coderack.codelets_run % self.activation_update_frequency == 0:
                    self.bubble_chamber.loggers["structure"].log_concepts_and_frames(
                        self.bubble_chamber, self.coderack
                    )
                    self.print_status_update()
                    self.bubble_chamber.spread_activations()
                    self.bubble_chamber.update_activations()
                if self.coderack.codelets_run >= 5000:
                    raise NoMoreCodelets
                self.coderack.select_and_run_codelet()
            except NoMoreCodelets:
                self.loggers["error"].log("No more codelets.")
                self.print_results()
                break
            except Exception as e:
                raise e
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
