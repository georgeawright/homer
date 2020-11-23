import random
from typing import List

from .bubble_chamber import BubbleChamber
from .codelet import Codelet
from .codelets import FactoryCodelet
from .errors import NoMoreCodelets
from .hyper_parameters import HyperParameters
from .logger import Logger


class Coderack:

    IDEAL_POPULATION = HyperParameters.IDEAL_CODERACK_POPULATION
    MINIMUM_CODELET_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY

    def __init__(
        self, bubble_chamber: BubbleChamber, codelets: List[Codelet], logger: Logger
    ):
        self.bubble_chamber = bubble_chamber
        self._codelets = codelets
        self.codelets_run = 0
        self.logger = logger

    @classmethod
    def setup(cls, bubble_chamber: BubbleChamber, logger: Logger):
        codelets = [FactoryCodelet.spawn("coderack", bubble_chamber, 1.0)]
        return cls(bubble_chamber, codelets, logger)

    def add_codelet(self, codelet: Codelet):
        if codelet.urgency > self.MINIMUM_CODELET_URGENCY:
            self.logger.log(codelet)
            self._codelets.append(codelet)

    def select_and_run_codelet(self):
        codelet = self.select_codelet()
        self.logger.log_codelet_run(codelet)
        codelet.run()
        self.codelets_run += 1
        for child_codelet in codelet.child_codelets:
            self.add_codelet(child_codelet)

    def select_codelet(self) -> Codelet:
        codelet_choice = None
        highest_weight = 0
        for codelet in self._codelets:
            weight = codelet.urgency + random.random() * self._randomness()
            if weight > highest_weight:
                highest_weight = weight
                codelet_choice = codelet
        if codelet_choice is None:
            raise NoMoreCodelets
        if self.codelets_run > 10000:
            raise NoMoreCodelets
        self._codelets.remove(codelet_choice)
        return codelet_choice

    def _randomness(self) -> float:
        return 1 - self.bubble_chamber.top_level_working_space.quality
