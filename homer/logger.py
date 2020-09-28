from abc import ABC, abstractmethod
from typing import Any


class Logger(ABC):
    @abstractmethod
    def log(self, item: Any):
        pass

    @abstractmethod
    def log_codelet_run(self, codelet):
        pass
