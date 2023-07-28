import time
from typing import Dict

from .bubble_chamber import BubbleChamber
from .codelet import Codelet
from .codelets import (
    Builder,
    CoderackCleaner,
    Evaluator,
    Factory,
    FocusSetter,
    FocusUnsetter,
    GarbageCollector,
    Publisher,
    Selector,
    Suggester,
    Recycler,
    WorldviewSetter,
)
from .codelets.factories import (
    ConceptDrivenFactory,
    ViewDrivenFactory,
)
from .codelets.factories.bottom_up_factories import (
    BottomUpEvaluatorFactory,
    BottomUpSuggesterFactory,
)
from .errors import MissingStructureError, NoMoreCodelets
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters
from .logger import Logger


class Coderack:
    PROTECTED_CODELET_TYPES = (
        CoderackCleaner,
        Factory,
        FocusSetter,
        FocusUnsetter,
        GarbageCollector,
        Publisher,
        Recycler,
        WorldviewSetter,
    )

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        hyper_parameters: HyperParameters,
        loggers: Dict[str, Logger],
    ):
        self.bubble_chamber = bubble_chamber
        self.hyper_parameters = hyper_parameters
        self.MAXIMUM_POPULATION = hyper_parameters.MAXIMUM_CODERACK_POPULATION
        self.MINIMUM_CODELET_URGENCY = hyper_parameters.MINIMUM_CODELET_URGENCY
        self._codelets = []
        self.recently_run = set()
        self.codelets_run = 0
        self.loggers = loggers
        self.codelet_times = []

    @classmethod
    def setup(
        cls,
        bubble_chamber: BubbleChamber,
        hyper_parameters: HyperParameters,
        loggers: Dict[str, Logger],
    ):
        MINIMUM_CODELET_URGENCY = hyper_parameters.MINIMUM_CODELET_URGENCY
        coderack = cls(bubble_chamber, hyper_parameters, loggers)
        meta_codelets = [
            Publisher.spawn(
                "", bubble_chamber, coderack, 0.0, 0, MINIMUM_CODELET_URGENCY
            ),
            GarbageCollector.spawn(
                "", bubble_chamber, coderack, MINIMUM_CODELET_URGENCY
            ),
            Recycler.spawn("", bubble_chamber, coderack, MINIMUM_CODELET_URGENCY),
            FocusSetter.spawn("", bubble_chamber, coderack, MINIMUM_CODELET_URGENCY),
            WorldviewSetter.spawn(
                "", bubble_chamber, coderack, MINIMUM_CODELET_URGENCY
            ),
            CoderackCleaner.spawn(
                "", bubble_chamber, coderack, 0.0, MINIMUM_CODELET_URGENCY
            ),
            ConceptDrivenFactory.spawn(
                "", bubble_chamber, coderack, MINIMUM_CODELET_URGENCY
            ),
            ViewDrivenFactory.spawn(
                "", bubble_chamber, coderack, MINIMUM_CODELET_URGENCY
            ),
            BottomUpEvaluatorFactory.spawn(
                "", bubble_chamber, coderack, MINIMUM_CODELET_URGENCY
            ),
            BottomUpSuggesterFactory.spawn(
                "", bubble_chamber, coderack, MINIMUM_CODELET_URGENCY
            ),
        ]
        for codelet in meta_codelets:
            coderack.add_codelet(codelet)
        return coderack

    @property
    def population_size(self) -> int:
        return len(self._codelets)

    def add_codelet(self, codelet: Codelet):
        if codelet.urgency < self.MINIMUM_CODELET_URGENCY:
            return
        if not isinstance(codelet, self.PROTECTED_CODELET_TYPES):
            for existing_codelet in self._codelets:
                if isinstance(codelet, (Builder, Evaluator, Suggester)):
                    if (
                        type(codelet) == type(existing_codelet)
                        and codelet.targets == existing_codelet.targets
                    ):
                        existing_codelet.urgency = FloatBetweenOneAndZero(
                            existing_codelet.urgency + codelet.urgency
                        )
                        return
                if isinstance(codelet, Selector):
                    if (
                        type(codelet) == type(existing_codelet)
                        and codelet.champions == existing_codelet.champions
                        and codelet.challengers == existing_codelet.challengers
                    ):
                        existing_codelet.urgency = (
                            existing_codelet.urgency + codelet.urgency
                        )
                        return
        try:
            coderack_cleaner = [
                c for c in self._codelets if isinstance(c, CoderackCleaner)
            ][0]
            coderack_cleaner.urgency = FloatBetweenOneAndZero(
                self.population_size / self.MAXIMUM_POPULATION
            )
        except IndexError:
            pass
        self._codelets.append(codelet)

    def remove_codelet(self, codelet: Codelet):
        if not isinstance(codelet, self.PROTECTED_CODELET_TYPES):
            self._codelets.remove(codelet)

    def select_and_run_codelet(self):
        self.bubble_chamber.random_machine.codelets_run = self.codelets_run
        self.bubble_chamber.recalculate_satisfaction()
        codelet = self._select_a_codelet()
        self.loggers["activity"].log_codelet_start(codelet)
        codelet_start_time = time.time()
        if HyperParameters.TESTING:
            try:
                codelet.run()
            except Exception:
                self.loggers["activity"].log_codelet_end(self.population_size)
                self.loggers["error"].log(codelet)
        else:
            try:
                codelet.run()
            except Exception as e:
                self.loggers["activity"].log_codelet_end(self.population_size)
                raise e
        codelet_end_time = time.time()
        self.codelet_times.append(
            {
                "id": codelet.codelet_id,
                "type": type(codelet),
                "start": codelet_start_time,
                "end": codelet_end_time,
            }
        )
        self.recently_run.add(type(codelet))
        self.codelets_run += 1
        for child_codelet in codelet.child_codelets:
            self.add_codelet(child_codelet)
        self.loggers["activity"].log_codelet_end(self.population_size)

    def _select_a_codelet(self) -> Codelet:
        try:
            codelet_choice = self.bubble_chamber.random_machine.select(
                self._codelets, key=lambda x: x.urgency
            )
        except MissingStructureError:
            raise NoMoreCodelets
        self._codelets.remove(codelet_choice)
        return codelet_choice

    def _remove_a_codelet(self):
        codelet_choice = self.bubble_chamber.random_machine.select(
            self._codelets, key=lambda x: 1 - x.urgency
        )
        self.remove_codelet(codelet_choice)

    def proportion_of_codelets_of_type(self, t: type) -> float:
        try:
            return self.number_of_codelets_of_type(t) / len(self._codelets)
        except ZeroDivisionError:
            return 0.0

    def number_of_codelets_of_type(self, t: type) -> int:
        return sum(1 for codelet in self._codelets if isinstance(codelet, t))

    def _randomness(self) -> float:
        return 1 - self.bubble_chamber.satisfaction
