import random
import statistics
from typing import List, Union

from .logger import Logger
from .problem import Problem
from .structures import Space


class BubbleChamber:
    def __init__(
        self,
        top_level_working_space: Space,
        top_level_conceptual_space: Space,
        logger: Logger,
    ):
        self.top_level_working_space = top_level_working_space
        self.top_level_conceptual_space = top_level_conceptual_space
        self.logger = logger
        self.result = None

    @classmethod
    def setup(cls, problem: Problem, logger: Logger):
        pass

    def update_activations(self) -> None:
        pass
