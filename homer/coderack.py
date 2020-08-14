import random

from homer.codelet import BubbleChamber
from homer.codelet import Codelet
from homer.errors import NoMoreCodelets
from homer.logger import Logger


class Coderack:
    def __init__(self, bubble_chamber: BubbleChamber, logger: Logger):
        self.bubble_chamber = bubble_chamber
        self._codelets = []
        self.codelets_run = 0
        self.logger = logger

    def add_codelet(self, codelet: Codelet):
        self.logger.log(codelet)
        self._codelets.append(codelet)

    def select_and_run_codelet(self):
        codelet = self.select_codelet()
        follow_up = codelet.run()
        self.codelets_run += 1
        if follow_up is not None:
            self.add_codelet(follow_up)

    def select_codelet(self) -> Codelet:
        if len(self._codelets) < 1:
            self.get_more_codelets()
        codelet_choice = None
        highest_weight = 0
        for codelet in self._codelets:
            weight = codelet.urgency + random.random() * self._randomness()
            if weight > highest_weight:
                highest_weight = weight
                codelet_choice = codelet
        if codelet_choice is None:
            raise NoMoreCodelets
        self._codelets.remove(codelet_choice)
        return codelet_choice

    def get_more_codelets(self):
        for concept in self.bubble_chamber.concept_space.spawning_concepts:
            codelet = concept.spawn_codelet(self.bubble_chamber)
            if codelet is not None:
                self.add_codelet(codelet)

    def _randomness(self) -> float:
        return 1 - self.bubble_chamber.satisfaction
