from typing import Dict

from .bubble_chamber import BubbleChamber
from .codelets.suggesters import ChunkSuggester
from .coderack import Coderack
from .errors import NoMoreCodelets
from .hyper_parameters import HyperParameters
from .id import ID
from .interpreter import Interpreter
from .logger import Logger


class Linguoplotter:
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        coderack: Coderack,
        interpreter: Interpreter,
        hyper_parameters: HyperParameters,
        loggers: Dict[str, Logger],
        activation_update_frequency: int = HyperParameters.ACTIVATION_UPDATE_FREQUENCY,
    ):
        self.bubble_chamber = bubble_chamber
        self.coderack = coderack
        self.interpreter = interpreter
        self.hyper_parameters = hyper_parameters
        self.loggers = loggers
        self.activation_update_frequency = activation_update_frequency
        self.CODELET_RUN_LIMIT = self.hyper_parameters.CODELET_RUN_LIMIT
        self.NUMBER_OF_START_CHUNK_SUGGESTERS = (
            self.hyper_parameters.NUMBER_OF_START_CHUNK_SUGGESTERS
        )

    @classmethod
    def setup(
        cls,
        hyper_parameters: HyperParameters,
        loggers: Dict[str, Logger],
        random_seed: int = None,
    ):
        ID.reset()
        bubble_chamber = BubbleChamber.setup(
            hyper_parameters, loggers, random_seed=random_seed
        )
        coderack = Coderack.setup(bubble_chamber, hyper_parameters, loggers)
        loggers["structure"].coderack = coderack
        interpreter = Interpreter(bubble_chamber)
        return cls(bubble_chamber, coderack, interpreter, hyper_parameters, loggers)

    def run_program(self, program: str):
        self.interpreter.interpret_string(program)
        return self.run()

    def reset(self, loggers: Dict[str, Logger]):
        self.bubble_chamber.reset(loggers)
        self.coderack = Coderack.setup(self.bubble_chamber, loggers)
        loggers["structure"].coderack = self.coderack

    def run(self):
        for _ in range(self.NUMBER_OF_START_CHUNK_SUGGESTERS):
            self.coderack.add_codelet(ChunkSuggester.make("", self.bubble_chamber, 1.0))
        while self.bubble_chamber.result is None:
            try:
                if self.coderack.codelets_run % self.activation_update_frequency == 0:
                    if not self.hyper_parameters.TESTING:
                        self.print_status_update()
                    self.bubble_chamber.update_activations()
                if self.coderack.codelets_run >= self.CODELET_RUN_LIMIT:
                    raise NoMoreCodelets
                self.coderack.select_and_run_codelet()
            except NoMoreCodelets:
                self.loggers["error"].log_message("No more codelets.")
                break
            except Exception as e:
                raise e
        self.print_results()
        return {
            "random_seed": self.bubble_chamber.random_machine.seed,
            "result": self.bubble_chamber.result,
            "worldview": self.bubble_chamber.worldview.view.structure_id
            if self.bubble_chamber.worldview.view is not None
            else "None",
            "satisfaction": self.bubble_chamber.worldview.satisfaction,
            "codelets_run": self.coderack.codelets_run,
        }

    def print_status_update(self):
        codelets_run = self.coderack.codelets_run
        satisfaction = round(self.bubble_chamber.satisfaction, 3)
        determinism = round(self.bubble_chamber.random_machine.determinism, 3)
        coderack_population = len(self.coderack._codelets)
        view_count = len(self.bubble_chamber.views)
        focus = (
            self.bubble_chamber.focus.view.structure_id
            + self.bubble_chamber.focus.view.parent_frame.name
            if self.bubble_chamber.focus.view is not None
            else None
        )
        focus_unhappiness = (
            round(self.bubble_chamber.focus.view.unhappiness, 3)
            if self.bubble_chamber.focus.view is not None
            else "-"
        )
        focus_satisfaction = (
            round(self.bubble_chamber.focus.satisfaction, 3)
            if self.bubble_chamber.focus.view is not None
            else "-"
        )
        print("=" * 80)
        print(
            f"{codelets_run}: S={satisfaction}; D={determinism}; "
            + f"Coderack: {coderack_population}; "
            + f"Views: {view_count}; "
            + f"RecycleBin: {len(self.bubble_chamber.recycle_bin)}\n"
            + f"Focus: {focus} (Unhappiness: {focus_unhappiness}; Satisfaction: {focus_satisfaction})"
        )
        if self.bubble_chamber.worldview.view is not None:
            view_output = self.bubble_chamber.worldview.output
            print(view_output)

    def print_results(self):
        print(
            f"Seed: {self.bubble_chamber.random_machine.seed} | "
            + f"Codelets run: {self.coderack.codelets_run} | "
            + f"Satisfaction: {self.bubble_chamber.worldview.satisfaction} |"
        )
        print(f"Result: {self.bubble_chamber.result}")
