import random

from .bubble_chamber import BubbleChamber
from .codelet import Codelet
from .codelets import CoderackCleaner, Factory
from .codelets.factories import ConceptDrivenFactory, RandomFactory, RationalFactory
from .errors import NoMoreCodelets
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters
from .logger import Logger


class Coderack:

    MAXIMUM_POPULATION = HyperParameters.MAXIMUM_CODERACK_POPULATION
    MINIMUM_CODELET_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY

    def __init__(self, bubble_chamber: BubbleChamber, logger: Logger):
        self.bubble_chamber = bubble_chamber
        self._codelets = []
        self.recently_run = set()
        self.codelets_run = 0
        self.logger = logger

    @classmethod
    def setup(cls, bubble_chamber: BubbleChamber, logger: Logger):
        coderack = cls(bubble_chamber, logger)
        meta_codelets = [
            CoderackCleaner.spawn("", bubble_chamber, coderack, 0.0, 1.0),
            ConceptDrivenFactory.spawn("", bubble_chamber, coderack, 1.0),
            RandomFactory.spawn("", bubble_chamber, coderack, 1.0),
            RationalFactory.spawn("", bubble_chamber, coderack, 1.0),
        ]
        for codelet in meta_codelets:
            coderack.add_codelet(codelet)
        return coderack

    def add_codelet(self, codelet: Codelet):
        if codelet.urgency < self.MINIMUM_CODELET_URGENCY:
            return
        while len(self._codelets) >= self.MAXIMUM_POPULATION:
            self._remove_a_codelet()
        self.logger.log(codelet)
        self._codelets.append(codelet)

    def remove_codelet(self, codelet: Codelet):
        if not isinstance(codelet, (CoderackCleaner, Factory)):
            self._codelets.remove(codelet)

    def select_and_run_codelet(self):
        codelet = self._select_a_codelet()
        codelet.run()
        self.recently_run.add(type(codelet))
        self.logger.log_codelet_run(codelet)
        self.codelets_run += 1
        for child_codelet in codelet.child_codelets:
            self.add_codelet(child_codelet)

    def _select_a_codelet(self) -> Codelet:
        codelet_choice = None
        highest_weight = 0
        randomness = self._randomness()
        rationality = 1 - randomness
        for codelet in self._codelets:
            weight = codelet.urgency * rationality + random.random() * randomness
            if weight > highest_weight:
                highest_weight = weight
                codelet_choice = codelet
        if codelet_choice is None:
            raise NoMoreCodelets
        self._codelets.remove(codelet_choice)
        return codelet_choice

    def _remove_a_codelet(self):
        codelet_choice = None
        lowest_weight = float("inf")
        randomness = self._randomness()
        rationality = 1 - randomness
        for codelet in self._codelets:
            weight = codelet.urgency * rationality + random.random() * randomness
            if weight < lowest_weight:
                lowest_weight = weight
                codelet_choice = codelet
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
