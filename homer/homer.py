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
    CODELET_RUN_LIMIT = HyperParameters.CODELET_RUN_LIMIT

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
        loggers["structure"].coderack = coderack
        interpreter = Interpreter(bubble_chamber)
        return cls(bubble_chamber, coderack, interpreter, loggers)

    def run_program(self, program: str):
        self.interpreter.interpret_string(program)
        return self.run()

    def reset(self, loggers: Dict[str, Logger]):
        self.bubble_chamber.reset(loggers)
        self.coderack = Coderack.setup(self.bubble_chamber, loggers)
        loggers["structure"].coderack = self.coderack

    def run(self):
        while self.bubble_chamber.result is None:
            try:
                if self.coderack.codelets_run % self.activation_update_frequency == 0:
                    self.bubble_chamber.loggers["structure"].log_concepts_and_frames(
                        self.bubble_chamber, self.coderack
                    )
                    for input_space in self.bubble_chamber.input_spaces:
                        self.bubble_chamber.loggers["structure"].log_contextual_space(
                            input_space, self.coderack
                        )
                    self.print_status_update()
                    self.bubble_chamber.spread_activations()
                    self.bubble_chamber.update_activations()
                if self.coderack.codelets_run >= self.CODELET_RUN_LIMIT:
                    raise NoMoreCodelets
                self.coderack.select_and_run_codelet()
            except NoMoreCodelets:
                self.loggers["errors"].log_message("No more codelets.")
                self.print_results()
                break
            except Exception as e:
                raise e
        self.print_results()
        return {
            "random_seed": self.bubble_chamber.random_machine.seed,
            "result": self.bubble_chamber.result,
            "satisfaction": self.bubble_chamber.satisfaction,
            "codelets_run": self.coderack.codelets_run,
        }

    def print_status_update(self):
        codelets_run = self.coderack.codelets_run
        bubble_chamber_satisfaction = self.bubble_chamber.satisfaction
        suggest_activation = self.bubble_chamber.concepts["suggest"].activation
        build_activation = self.bubble_chamber.concepts["build"].activation
        evaluate_activation = self.bubble_chamber.concepts["evaluate"].activation
        select_activation = self.bubble_chamber.concepts["select"].activation
        focus = (
            self.bubble_chamber.focus.view.structure_id
            + self.bubble_chamber.focus.view.parent_frame.name
            if self.bubble_chamber.focus.view is not None
            else None
        )
        focus_unhappiness = (
            self.bubble_chamber.focus.view.unhappiness
            if self.bubble_chamber.focus.view is not None
            else "-"
        )
        focus_satisfaction = (
            self.bubble_chamber.focus.satisfaction
            if self.bubble_chamber.focus.view is not None
            else "-"
        )
        print("=" * 200)
        print(
            f"codelets run: {codelets_run}; "
            + f"satisf.: {bubble_chamber_satisfaction}; "
            + f"SUGGEST: {suggest_activation}; "
            + f"BUILD: {build_activation}; "
            + f"EVALUATE: {evaluate_activation}; "
            + f"SELECT: {select_activation}; "
            + f"Focus: {focus} (unhappy: {focus_unhappiness}; satisf.: {focus_satisfaction})"
        )
        if self.bubble_chamber.worldview.view is not None:
            view_output = self.bubble_chamber.worldview.view.output_space
            main_chunk = view_output.contents.filter(
                lambda x: x.is_chunk and x.super_chunks.is_empty()
            ).get()
            text = main_chunk.name
            print(text)
        print("=" * 200)

    def print_results(self):
        print(f"codelets run: {self.coderack.codelets_run}")
        print(f"satisfaction: {self.bubble_chamber.worldview.satisfaction}")
        print(f"result: {self.bubble_chamber.result}")
