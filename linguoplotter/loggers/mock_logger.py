from typing import Any
from linguoplotter.logger import Logger


class MockLogger(Logger):
    def log(self, item: Any):
        pass

    def __getattr__(self, name: str):
        return lambda *args: None
