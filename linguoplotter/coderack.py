import statistics
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
    ExigentStructureConceptDrivenFactory,
)
from .errors import MissingStructureError, NoMoreCodelets
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters
from .logger import Logger


class Coderack:

    MAXIMUM_POPULATION = HyperParameters.MAXIMUM_CODERACK_POPULATION
    MINIMUM_CODELET_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY
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

    def __init__(self, bubble_chamber: BubbleChamber, loggers: Dict[str, Logger]):
        self.bubble_chamber = bubble_chamber
        self._codelets = []
        self.recently_run = set()
        self.codelets_run = 0
        self.loggers = loggers

    @classmethod
    def setup(cls, bubble_chamber: BubbleChamber, loggers: Dict[str, Logger]):
        coderack = cls(bubble_chamber, loggers)
        meta_codelets = [
            Publisher.spawn("", bubble_chamber, cls.MINIMUM_CODELET_URGENCY),
            GarbageCollector.spawn(
                "", bubble_chamber, coderack, cls.MINIMUM_CODELET_URGENCY
            ),
            Recycler.spawn("", bubble_chamber, coderack, cls.MINIMUM_CODELET_URGENCY),
            FocusSetter.spawn(
                "", bubble_chamber, coderack, cls.MINIMUM_CODELET_URGENCY
            ),
            WorldviewSetter.spawn(
                "", bubble_chamber, coderack, cls.MINIMUM_CODELET_URGENCY
            ),
            CoderackCleaner.spawn(
                "", bubble_chamber, coderack, 0.0, cls.MINIMUM_CODELET_URGENCY
            ),
            ConceptDrivenFactory.spawn(
                "", bubble_chamber, coderack, cls.MINIMUM_CODELET_URGENCY
            ),
            ViewDrivenFactory.spawn(
                "", bubble_chamber, coderack, cls.MINIMUM_CODELET_URGENCY
            ),
            ExigentStructureConceptDrivenFactory.spawn(
                "", bubble_chamber, coderack, cls.MINIMUM_CODELET_URGENCY
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
                if isinstance(codelet, Suggester) or isinstance(codelet, Builder):
                    if (
                        type(codelet) == type(existing_codelet)
                        and codelet.targets_dict == existing_codelet.targets_dict
                    ):
                        existing_codelet.urgency = statistics.fmean(
                            [codelet.urgency, existing_codelet.urgency]
                        )
                        return
                if isinstance(codelet, Evaluator):
                    if (
                        type(codelet) == type(existing_codelet)
                        and codelet.target_structures
                        == existing_codelet.target_structures
                    ):
                        existing_codelet.urgency = statistics.fmean(
                            [codelet.urgency, existing_codelet.urgency]
                        )
                        return
                if isinstance(codelet, Selector):
                    if (
                        type(codelet) == type(existing_codelet)
                        and codelet.champions == existing_codelet.champions
                        and codelet.challengers == existing_codelet.challengers
                    ):
                        existing_codelet.urgency = statistics.fmean(
                            [codelet.urgency, existing_codelet.urgency]
                        )
                        return
        self._codelets.append(codelet)

    def remove_codelet(self, codelet: Codelet):
        if not isinstance(codelet, self.PROTECTED_CODELET_TYPES):
            self._codelets.remove(codelet)

    def select_and_run_codelet(self):
        codelet = self._select_a_codelet()
        if HyperParameters.TESTING:
            try:
                codelet.run()
            except Exception:
                self.bubble_chamber.loggers["error"].log(codelet)
        else:
            codelet.run()
        self.bubble_chamber.recalculate_satisfaction()
        if self.bubble_chamber.focus.view is not None:
            self.bubble_chamber.focus.spaces_quality_history.append(
                self.bubble_chamber.focus.satisfaction
            )
        self.recently_run.add(type(codelet))
        self.codelets_run += 1
        view_count = len(self.bubble_chamber.views)
        self.loggers["activity"].log(
            codelet,
            f"Time: {self.codelets_run} | "
            + f"Satisfaction: {self.bubble_chamber.satisfaction} | "
            + f"Coderack Population Size: {self.population_size} | "
            + f"View Count: {view_count}\n"
            + f"Focus: {self.bubble_chamber.focus.view}\n"
            + f"Worldview: {self.bubble_chamber.worldview.view}\n",
        )
        for child_codelet in codelet.child_codelets:
            self.add_codelet(child_codelet)

    def _select_a_codelet(self) -> Codelet:
        if len(self._codelets) >= self.MAXIMUM_POPULATION:
            codelet_choice = [
                codelet
                for codelet in self._codelets
                if isinstance(codelet, CoderackCleaner)
            ][0]
            self._codelets.remove(codelet_choice)
            return codelet_choice
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
