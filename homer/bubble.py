from abc import ABC, abstractmethod
from typing import List, Optional, Union

from .activation_pattern import ActivationPattern


class Bubble:
    def __init__(self, activation: ActivationPattern, bubble_id: str):
        self.activation = activation
        self.bubble_id = bubble_id

    @abstractmethod
    def spread_activation(self):
        pass
