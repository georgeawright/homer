import random

from .bubble_chamber import BubbleChamber
from .codelet import Codelet
from .hyper_parameters import HyperParameters
from .logger import Logger


class Coderack:

    MINIMUM_CODELET_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY
    URGENCY_THRESHOLD_STEP_SIZE = HyperParameters.CODERACK_URGENCY_THRESHOLD_STEP_SIZE

    def __init__(self, bubble_chamber: BubbleChamber, logger: Logger):
        self.bubble_chamber = bubble_chamber
        self._codelets = []
        self.codelets_run = 0
        self.logger = logger

    def select_and_run_codelet(self):
        codelet = self._select_codelet()
        self.logger.log_codelet_run(codelet)
        codelet.run()
        self.codelets_run += 1
        for child_codelet in codelet.child_codelets:
            self._add_codelet(child_codelet)

    def _select_codelet(self) -> Codelet:
        urgency_threshold = self.bubble_chamber.concept_space[
            "satisfaction"
        ].activation.as_scalar()
        codelet_choice = random.choice(self._codelets)
        while codelet_choice.urgency < urgency_threshold:
            urgency_threshold -= self.URGENCY_THRESHOLD_STEP_SIZE
            codelet_choice = random.choice(self._codelets)
        self._codelets.remove(codelet_choice)
        return codelet_choice

    def _add_codelet(self, codelet: Codelet):
        if codelet.urgency > self.MINIMUM_CODELET_URGENCY:
            self.logger.log(codelet)
            self._codelets.append(codelet)
